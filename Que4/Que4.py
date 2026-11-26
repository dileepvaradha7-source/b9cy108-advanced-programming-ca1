"""Extract Dublin postal districts, export JSON and CSV, and print the CSV."""

import argparse
import csv
import json
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


SOURCE = "https://en.wikipedia.org/wiki/List_of_Dublin_postal_districts"
DISTRICT_HEADING = re.compile(r"Dublin \d+(?: West)? \((D\d+W?)\)")
EXPECTED_CODES = {f"D{number}" for number in range(1, 19)} | {"D6W", "D20", "D22", "D24"}
AREA_SEPARATOR = re.compile(r"(?:,\s*(?:and\s+)?|\s+and\s+)(?![^()]*\))")
QUALIFIER = re.compile(r"^(?:the |most of |parts? of |central |lower |upper )+")


def fetch_page():
    request = Request(SOURCE, headers={"User-Agent": "B9CY108-DublinDistricts/1.0 (coursework)"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def names_from(description):
    description = description.split(" and contains ", 1)[0]
    names = []
    for item in AREA_SEPARATOR.split(description):
        area, _, detail = item.partition(" (")
        area = re.sub(r"\s+(?:east|west) of Ballymun Road$", "", area)
        area = QUALIFIER.sub("", area).strip()
        if area:
            names.append(area)
        if detail.startswith("including "):
            names.extend(names_from(detail.removeprefix("including ").rstrip(")")))
    return names


def extract_districts(html):
    soup = BeautifulSoup(html, "html.parser")
    for footnote in soup.select("sup.reference"):
        footnote.decompose()

    districts = {}
    for heading in soup.find_all("h2"):
        heading_match = DISTRICT_HEADING.fullmatch(heading.get_text(" ", strip=True))
        if heading_match is None:
            continue
        district = heading_match.group(1)
        if district in districts:
            raise ValueError(f"Duplicate district heading {district}.")

        wrapper = heading.parent
        boundary = wrapper if "mw-heading" in wrapper.get("class", []) else heading
        paragraph = next((tag for tag in boundary.find_next_siblings()
                          if tag.name == "p" or tag.name == "h2"
                          or "mw-heading" in tag.get("class", [])), None)
        if paragraph is None or paragraph.name != "p":
            raise ValueError(f"No district description found for {district}.")
        description = re.sub(r"\s+", " ", paragraph.get_text()).strip()
        lead, _, remainder = description.partition(". ")
        lead = lead.rstrip(".")
        # D1 and D2 introduce their lists after a general description of the city centre.
        area_list = re.split(r", including | and takes in areas around ", lead, maxsplit=1)
        if len(area_list) == 1:
            area_list = re.split(r" includes (?:areas such as )?", lead, maxsplit=1)
        if len(area_list) != 2:
            raise ValueError(f"Could not identify the area list for {district}.")
        names = names_from(area_list[1])
        additional = re.match(r"Dublin \d+ also covers (.+?) areas\.", remainder)
        if additional:
            names.extend(names_from(additional.group(1)))
        if not names:
            raise ValueError(f"No areas extracted for {district}.")
        districts[district] = list(dict.fromkeys(names))

    if districts.keys() != EXPECTED_CODES:
        missing = ", ".join(sorted(EXPECTED_CODES - districts.keys()))
        extra = ", ".join(sorted(districts.keys() - EXPECTED_CODES))
        raise ValueError(f"Unexpected district set. Missing: {missing or 'none'}. Extra: {extra or 'none'}.")
    return districts


def export_and_print(districts, directory):
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / "dublin_postal_districts.json"
    csv_path = directory / "dublin_postal_districts.csv"
    json_path.write_text(json.dumps(districts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    records = json.loads(json_path.read_text(encoding="utf-8"))
    with csv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("district_code", "area_name"))
        writer.writerows((code, area) for code, areas in records.items() for area in areas)

    with csv_path.open(encoding="utf-8", newline="") as saved:
        reader = csv.reader(saved)
        heading = next(reader)
        print(f"{heading[0]:<14} {heading[1]}")
        count = 0
        for code, area in reader:
            print(f"{code:<14} {area}")
            count += 1
    print(f"Printed {count} CSV rows from {len(records)} districts.")
    print(f"Saved {json_path.name} and {csv_path.name}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        export_and_print(extract_districts(fetch_page()), args.output_dir)
    except (URLError, OSError, ValueError) as error:
        print(f"Could not export Dublin postal districts: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
