import argparse
import os
from parser import parse_csv_file
from database import save_db, load_db
from queries import run_queries

def main():
    parser = argparse.ArgumentParser(description="Flight Schedule Parser")
    parser.add_argument("-i", help="Input CSV file")
    parser.add_argument("-d", help="Input directory with CSV files")
    parser.add_argument("-o", help="Output JSON file", default="db.json")
    parser.add_argument("-j", help="Load existing JSON database")
    parser.add_argument("-q", help="Query JSON file")

    args = parser.parse_args()

    flights = []
    errors = []

    if args.j:
        flights = load_db(args.j)
    else:
        if args.i:
            v, e = parse_csv_file(args.i)
            flights.extend(v)
            errors.extend(e)

        if args.d:
            for file in os.listdir(args.d):
                if file.endswith(".csv"):
                    v, e = parse_csv_file(os.path.join(args.d, file))
                    flights.extend(v)
                    errors.extend(e)

        save_db(flights, args.o)

        if errors:
            with open("errors.txt", "w") as f:
                for err in errors:
                    f.write(err + "\n")

    if args.q:
        run_queries(flights, args.q)

if __name__ == "__main__":
    main()
