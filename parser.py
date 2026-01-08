import csv
import re
from datetime import datetime

DATETIME_FMT = "%Y-%m-%d %H:%M"

def parse_csv_file(path):
    valid = []
    errors = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for line_no, row in enumerate(reader, start=1):
            if not row or row[0].startswith("#"):
                errors.append(f"Line {line_no}: {','.join(row)} → comment line, ignored for data parsing")
                continue

            if len(row) != 6:
                errors.append(f"Line {line_no}: {','.join(row)} → missing required fields")
                continue

            flight_id, origin, dest, dep, arr, price = row
            problems = []

            if not re.fullmatch(r"[A-Za-z0-9]{2,8}", flight_id):
                problems.append("invalid flight_id")

            if not re.fullmatch(r"[A-Z]{3}", origin):
                problems.append("invalid origin code")

            if not re.fullmatch(r"[A-Z]{3}", dest):
                problems.append("invalid destination code")

            try:
                dep_dt = datetime.strptime(dep, DATETIME_FMT)
            except:
                problems.append("invalid departure datetime")

            try:
                arr_dt = datetime.strptime(arr, DATETIME_FMT)
            except:
                problems.append("invalid arrival datetime")

            if "invalid departure datetime" not in problems and \
               "invalid arrival datetime" not in problems:
                if arr_dt <= dep_dt:
                    problems.append("arrival before departure")

            try:
                price_val = float(price)
                if price_val <= 0:
                    problems.append("negative price value")
            except:
                problems.append("invalid price")

            if problems:
                errors.append(
                    f"Line {line_no}: {','.join(row)} → " + ", ".join(problems)
                )
            else:
                valid.append({
                    "flight_id": flight_id,
                    "origin": origin,
                    "destination": dest,
                    "departure_datetime": dep,
                    "arrival_datetime": arr,
                    "price": price_val
                })

    return valid, errors
