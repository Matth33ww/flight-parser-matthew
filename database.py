import json

def save_db(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_db(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
