"""Collect library member details and register them over TCP."""

import argparse
import json
import socket
import sys


MAX_MESSAGE = 4096


def collect_registration():
    print("LIBRARY MEMBERSHIP REGISTRATION")
    request = {
        "full_name": input("Full name: ").strip(),
        "residential_address": input("Residential address: ").strip(),
        "contact_number": input("Contact number: ").strip(),
        "email": input("Email address: ").strip(),
    }
    while True:
        months = input("Membership duration (6 or 12 months): ").strip()
        if months in ("6", "12"):
            request["membership_months"] = int(months)
            return request
        print("Please enter 6 or 12.")


def send_registration(port, request):
    message = json.dumps(request, ensure_ascii=False).encode("utf-8") + b"\n"
    if len(message) > MAX_MESSAGE:
        raise ValueError("The registration is too long. Shorten the input and try again.")

    with socket.create_connection(("127.0.0.1", port), timeout=15) as connection:
        print(f"Connected to 127.0.0.1:{port} (TCP).")
        connection.sendall(message)
        print("Sent registration details.")
        with connection.makefile("rb") as reply:
            line = reply.readline(MAX_MESSAGE + 1)

    if not line or len(line) > MAX_MESSAGE or not line.endswith(b"\n"):
        raise ValueError("The server returned an incomplete response.")
    try:
        response = json.loads(line.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("The server returned invalid JSON.") from error
    if not isinstance(response, dict):
        raise ValueError("The server returned an unexpected response.")
    return response


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=5050)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    try:
        response = send_registration(args.port, collect_registration())
    except (EOFError, KeyboardInterrupt):
        print("\nRegistration cancelled.")
        return 1
    except (OSError, ValueError) as error:
        print(f"Registration failed: {error}", file=sys.stderr)
        return 1

    if response.get("ok") is True and isinstance(response.get("registration_number"), str):
        print(f"Registration successful. Your number is {response['registration_number']}.")
        return 0

    print(f"Registration rejected: {response.get('error', 'Unexpected server response.')}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
