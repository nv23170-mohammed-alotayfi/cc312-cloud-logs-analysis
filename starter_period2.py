"""
PL202 - Day 1 (Period 2) Starter File
Task: Cloud Log Cleaner + JSON Summary (Mini Project)

You will:
1) Read logs.txt
2) Keep ONLY valid lines (4 parts AND level is INFO/WARN/ERROR)
3) Write clean logs to clean_logs.txt (same original format)
4) Create summary.json with:
   - total_lines, valid_lines, invalid_lines
   - levels: counts of INFO/WARN/ERROR (valid only)
   - top_services: top 3 services by valid log count
   - top_errors: top 3 ERROR messages by count (valid ERROR only)

IMPORTANT:
- Work independently (no teacher / classmates).
- You may copy your solutions from Period 1.
"""

import json
from pathlib import Path
from collections import Counter

LOG_FILE = Path("logs.txt")
CLEAN_FILE = Path("clean_logs.txt")
SUMMARY_FILE = Path("summary.json")

ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line: str):
    """
    Returns (timestamp, level, service, message) OR None if format invalid.
    """
    line = line.strip()
    if not line:
        return None
    pass


def normalize_level(level: str) -> str:
    """Return uppercase level."""
    return level.upper()
    pass


def main():
    if not LOG_FILE.exists():
        print(f"ERROR: Could not find {LOG_FILE}. Make sure logs.txt is in the same folder.")
        return

    total_lines = 0
    valid_lines = 0
    invalid_lines = 0

    level_counts = {"INFO": 0, "WARN": 0, "ERROR": 0}

    service_counter = Counter()
    error_message_counter = Counter()

    clean_lines = []  # store valid lines to write later

    with LOG_FILE.open("r") as file:
        for line in file:
            total_lines += 1
            parsed = parse_line(line)
            
            if parsed is None:
                invalid_lines += 1
                continue
                
            timestamp, level, service, message = parsed
            norm_level = normalize_level(level)
            
            if norm_level not in ALLOWED_LEVELS:
                invalid_lines += 1
                continue
            
            # Now it's valid:
            valid_lines += 1
            level_counts[norm_level] += 1
            service_counter[service] += 1
            
            if norm_level == "ERROR":
                error_message_counter[message] += 1
                
            # Store formatted string: timestamp | LEVEL | service | message
            clean_lines.append(f"{timestamp} | {norm_level} | {service} | {message}")

    CLEAN_FILE.write_text("\n".join(clean_lines) + "\n")

    top_services = [
        {"service": s, "count": c} for s, c in service_counter.most_common(3)
    ]
    
    top_errors = [
        {"message": m, "count": c} for m, c in error_message_counter.most_common(3)
    ]

    summary_data = {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "invalid_lines": invalid_lines,
        "levels": level_counts,
        "top_services": top_services,
        "top_errors": top_errors
    }

    with SUMMARY_FILE.open("w") as json_file:
        json.dump(summary_data, json_file, indent=2)

    print(f"Analysis Complete!")
    print(f"Clean logs saved to: {CLEAN_FILE}")
    print(f"Summary JSON saved to: {SUMMARY_FILE}")
    print(f"Valid: {valid_lines}, Invalid: {invalid_lines}")
    pass


if __name__ == "__main__":
    main()
