"""Accept one library registration per TCP connection."""

import argparse
import json
import os
import re
import socketserver
import sys

import psycopg


MAX_MESSAGE = 4096
SCHEMA = """
CREATE TABLE IF NOT EXISTS library_members (
    registration_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name varchar(120) NOT NULL,
    residential_address varchar(250) NOT NULL,
    contact_number varchar(32) NOT NULL,
    email varchar(254) NOT NULL,
    membership_months smallint NOT NULL CHECK (membership_months IN (6, 12)),
    registered_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""
INSERT_MEMBER = """
INSERT INTO library_members
    (full_name, residential_address, contact_number, email, membership_months)
VALUES (%s, %s, %s, %s, %s)
RETURNING registration_id
"""


def validate(request):
    if not isinstance(request, dict):
        raise ValueError("Send a JSON object containing the registration fields.")

    fields = {}
    for key, label, limit in (
        ("full_name", "Full name", 120),
        ("residential_address", "Residential address", 250),
        ("contact_number", "Contact number", 32),
        ("email", "Email address", 254),
    ):
        value = request.get(key)
        if not isinstance(value, str) or not 1 <= len(value.strip()) <= limit:
            raise ValueError(f"{label} is required and must be at most {limit} characters.")
        if any(ord(character) < 32 for character in value):
            raise ValueError(f"{label} must be on one line.")
        fields[key] = value.strip()

    contact = fields["contact_number"]
    if not re.fullmatch(r"\+?[0-9 ()-]+", contact) or not 7 <= len(re.findall(r"[0-9]", contact)) <= 15:
        raise ValueError("Contact number must contain 7 to 15 digits.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", fields["email"]):
        raise ValueError("Enter a valid email address.")

    months = request.get("membership_months")
    if type(months) is not int or months not in (6, 12):
        raise ValueError("Membership duration must be 6 or 12 months.")

    return (fields["full_name"], fields["residential_address"], contact, fields["email"], months)


def database_connection():
    # An empty DSN lets libpq use PGHOST, PGPORT, PGDATABASE and PGUSER.
    return psycopg.connect(os.environ.get("LIBRARY_DATABASE_URL", ""), connect_timeout=5)


def register_member(fields):
    with database_connection() as connection:
        registration_id, = connection.execute(INSERT_MEMBER, fields).fetchone()
    return f"LIB-{registration_id:06d}"


class RegistrationHandler(socketserver.StreamRequestHandler):
    timeout = 10

    def handle(self):
        print(f"Client connected from {self.client_address[0]}.", flush=True)
        try:
            line = self.rfile.readline(MAX_MESSAGE + 1)
            if not line:
                return
            if len(line) > MAX_MESSAGE or not line.endswith(b"\n"):
                raise ValueError("Send one newline-terminated message of at most 4096 bytes.")
            try:
                request = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ValueError("Send valid UTF-8 JSON.") from error

            fields = validate(request)
            number = register_member(fields)
            response = {"ok": True, "registration_number": number}
            print(f"Saved registration {number} ({fields[-1]} months).", flush=True)
        except ValueError as error:
            response = {"ok": False, "error": str(error)}
            print("Rejected invalid registration.", flush=True)
        except psycopg.Error as error:
            print(f"Database write failed ({type(error).__name__}).", file=sys.stderr, flush=True)
            response = {"ok": False, "error": "Registration could not be saved. Try again later."}
        except TimeoutError:
            print("Client timed out before sending a complete request.", flush=True)
            return
        except OSError:
            print("Client disconnected during the request.", flush=True)
            return

        try:
            self.wfile.write(json.dumps(response).encode("utf-8") + b"\n")
            if response["ok"]:
                print(f"Sent {response['registration_number']} to the client.", flush=True)
        except OSError:
            print("Client disconnected before the response could be sent.", flush=True)


class RegistrationServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=5050)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    try:
        with database_connection() as connection:
            connection.execute(SCHEMA)
        with RegistrationServer(("127.0.0.1", args.port), RegistrationHandler) as server:
            print(f"Library server listening on 127.0.0.1:{args.port} (TCP).", flush=True)
            print("PostgreSQL is ready.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nLibrary server stopped.")
    except psycopg.Error as error:
        print(f"Cannot initialize PostgreSQL ({type(error).__name__}). Check the database settings.",
              file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Cannot start the server: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
