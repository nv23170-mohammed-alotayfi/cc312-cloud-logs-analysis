"""
PL202 - Day 1 (Period 1) Starter File
Task: Cloud Log Reader — Parse + Validate + Report (TXT)

You will:
1) Read logs.txt
2) Parse each line into: timestamp | level | service | message
3) Validate:
   - If a line does NOT have exactly 4 parts => invalid line
   - Normalize level to uppercase
   - Allowed levels: INFO, WARN, ERROR
   - Anything else => INVALID_LEVEL
4) Count totals and save the summary to period1_report.txt

IMPORTANT:
- Work independently (no teacher / classmates).
- Only fill the TODO parts. Do not delete other code.
"""

from pathlib import Path

LOG_FILE = Path("logs.txt")
OUTPUT_REPORT = Path("period1_report.txt")

ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line: str):
    """
    Parse a single log line.
    Returns a tuple: (timestamp, level, service, message) OR None if format is invalid.

    Expected format:
    timestamp | level | service | message
    """
    clean_line = line.strip()
    if not clean_line:
        return None
    parts = [part.strip() for part in clean_line.split('|')]
    if len(parts) != 4:
        return None
    return tuple(parts)
    pass


def normalize_level(level: str) -> str:
    """Normalize log level to uppercase."""
    return level.upper()    
    pass


def main():
    # Counters
    total_lines = 0
    invalid_lines = 0

    level_counts = {
        "INFO": 0,
        "WARN": 0,
        "ERROR": 0,
        "INVALID_LEVEL": 0,
    }

    # Safety check
    if not LOG_FILE.exists():
        print(f"ERROR: Could not find {LOG_FILE}. Make sure logs.txt is in the same folder.")
        return

    with LOG_FILE.open("r") as f:
        for line in f:
            total_lines += 1
           
            parsed = parse_line(line)
            if parsed is None:
                invalid_lines += 1
                continue
           
            # Unpack the tuple and normalize
            _, level, _, _ = parsed
            norm_level = normalize_level(level)
           
            # Update counts
            if norm_level in ALLOWED_LEVELS:
                level_counts[norm_level] += 1
            else:
                level_counts["INVALID_LEVEL"] += 1

    summary = f"""--- LOG ANALYSIS REPORT ---
Total Lines Processed: {total_lines}
Invalid Format Lines:  {invalid_lines}
---------------------------
INFO:          {level_counts['INFO']}
WARN:          {level_counts['WARN']}
ERROR:         {level_counts['ERROR']}
Unknown Level: {level_counts['INVALID_LEVEL']}
---------------------------
"""

    print(summary)

    OUTPUT_REPORT.write_text(summary)
    print(f"Report successfully saved to {OUTPUT_REPORT}")

    pass


if __name__ == "__main__":
    main()