import json
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"

def run_queries(flights, query_file):
    # Load queries from JSON file
    with open(query_file, encoding="utf-8") as f:
        queries = json.load(f)

    # Ensure queries is always a list
    if isinstance(queries, dict):
        queries = [queries]

    responses = []

    for q in queries:
        matches = flights

        if "flight_id" in q:
            matches = [f for f in matches if f["flight_id"] == q["flight_id"]]

        if "origin" in q:
            matches = [f for f in matches if f["origin"] == q["origin"]]

        if "destination" in q:
            matches = [f for f in matches if f["destination"] == q["destination"]]

        if "price" in q:
            matches = [f for f in matches if f["price"] <= q["price"]]

        if "departure_datetime" in q:
            limit = datetime.strptime(q["departure_datetime"], FMT)
            matches = [
                f for f in matches
                if datetime.strptime(f["departure_datetime"], FMT) >= limit
            ]

        if "arrival_datetime" in q:
            limit = datetime.strptime(q["arrival_datetime"], FMT)
            matches = [
                f for f in matches
                if datetime.strptime(f["arrival_datetime"], FMT) <= limit
            ]

        responses.append({
            "query": q,
            "matches": matches
        })

    # Creating response file with student details
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"response_241ADB032_Matthew_Manoah_Boddu_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2)
