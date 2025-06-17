import json
import csv
from pathlib import Path

INPUT_FILE = Path("logs/session_log.json")
OUTPUT_FILE = Path("logs/performance_metrics.csv")

def export_to_csv():
    with open(INPUT_FILE, "r") as infile:
        data = json.load(infile)

    with open(OUTPUT_FILE, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["timestamp", "input", "output", "latency"])
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Exported {len(data)} records to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_to_csv()
