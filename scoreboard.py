"""Summarize simple binary-outcome experiments."""
import argparse
import csv
import json
import math
import statistics


def summarize(rows):
    groups = {}
    for row in rows:
        name = row["variant"].strip()
        if not name:
            raise ValueError("variant cannot be blank")
        visitors = int(row["visitors"])
        conversions = int(row["conversions"])
        if visitors <= 0 or conversions < 0 or conversions > visitors:
            raise ValueError("invalid visitors or conversions")
        bucket = groups.setdefault(name, [0, 0])
        bucket[0] += visitors
        bucket[1] += conversions
    output = []
    for name, (visitors, conversions) in sorted(groups.items()):
        p = conversions / visitors
        z = 1.96
        denominator = 1 + z*z/visitors
        center = (p + z*z/(2*visitors)) / denominator
        half = z*math.sqrt(p*(1-p)/visitors + z*z/(4*visitors*visitors))/denominator
        output.append({"variant": name, "visitors": visitors, "conversions": conversions,
                       "conversion_rate": round(p, 5),
                       "wilson_95_interval": [round(max(0, center-half), 5), round(min(1, center+half), 5)]})
    return {"variants": output, "best_observed_variant": max(output, key=lambda item: item["conversion_rate"])["variant"] if output else None}


def run(path):
    with open(path, newline="", encoding="utf-8") as source:
        result = summarize(csv.DictReader(source))
    return result


def main():
    parser = argparse.ArgumentParser(description="Compare experiment conversion rates")
    parser.add_argument("csv_file")
    parser.add_argument("--output")
    args = parser.parse_args()
    report = json.dumps(run(args.csv_file), indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(report + "\n")
    else:
        print(report)


if __name__ == "__main__":
    main()
