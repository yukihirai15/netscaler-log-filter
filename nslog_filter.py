import argparse
import os
import re
from datetime import datetime

def parse_timestamp(line):
    """Try to extract a timestamp from the beginning of a NetScaler log line."""
    # Example NetScaler format: Oct 29 12:04:12
    try:
        parts = line.split()
        if len(parts) >= 3:
            ts_str = " ".join(parts[:3])
            return datetime.strptime(ts_str, "%b %d %H:%M:%S").replace(year=datetime.now().year)
    except Exception:
        return None
    return None


def extract_logs(path, keywords, output_file, use_regex=False, exclude=None, since=None, until=None):
    keywords = [k.strip() for k in keywords.split(",")]
    exclude = [e.strip().lower() for e in exclude.split(",")] if exclude else []
    results = []
    match_counts = {k: 0 for k in keywords}

    if os.path.isdir(path):
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.log')]
    else:
        files = [path]

    for file in files:
        if not os.path.exists(file):
            print(f"[!] File not found: {file}")
            continue

        with open(file, 'r', errors='ignore') as f:
            for line_no, line in enumerate(f, 1):
                line_stripped = line.strip()
                if not line_stripped:
                    continue

                # Timestamp filtering
                ts = parse_timestamp(line)
                if ts and since and ts < since:
                    continue
                if ts and until and ts > until:
                    continue

                # Exclude keyword filtering
                if any(ex in line.lower() for ex in exclude):
                    continue

                # Keyword or regex match
                matched = False
                if use_regex:
                    for kw in keywords:
                        if re.search(kw, line, re.IGNORECASE):
                            results.append(f"[{file}] Line {line_no}: {line_stripped}\n\n")
                            match_counts[kw] += 1
                            matched = True
                            break
                else:
                    line_lower = line.lower()
                    for kw in keywords:
                        if kw.lower() in line_lower:
                            results.append(f"[{file}] Line {line_no}: {line_stripped}\n\n")
                            match_counts[kw] += 1
                            matched = True
                            break

    # Prepare header
    header = (
        f"### NetScaler Log Keyword Extractor v2.0 ###\n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Path: {path}\n"
        f"Keywords: {', '.join(keywords)}\n"
        f"Excluded: {', '.join(exclude) if exclude else 'None'}\n"
        f"Regex Mode: {'Enabled' if use_regex else 'Disabled'}\n"
        f"Time Filter: "
        f"{since.strftime('%b %d %H:%M:%S') if since else 'Start'} → "
        f"{until.strftime('%b %d %H:%M:%S') if until else 'End'}\n"
        f"{'-'*60}\n\n"
    )

    # Write results
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(header)
        out.writelines(results)

    # Print summary
    print(f"\n[+] Log extraction complete → {output_file}")
    print(f"[+] Total matches: {sum(match_counts.values())}")
    print(f"[+] Keyword breakdown:")
    for kw, count in match_counts.items():
        print(f"    {kw}: {count}")
    print(f"[+] Total lines written: {len(results)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NetScaler Log Keyword Extractor v2.0")
    parser.add_argument("--path", required=True, help="Path to log file or folder")
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords or regex patterns")
    parser.add_argument("--output", default="filtered_logs.txt", help="Output file name")
    parser.add_argument("--regex", action="store_true", help="Enable regex-based search")
    parser.add_argument("--exclude", help="Comma-separated keywords to exclude")
    parser.add_argument("--since", help="Filter logs since this timestamp (e.g. 'Oct 28 10:00:00')")
    parser.add_argument("--until", help="Filter logs until this timestamp (e.g. 'Oct 28 18:00:00')")

    args = parser.parse_args()

    # Parse timestamps (optional)
    since_dt = datetime.strptime(args.since, "%b %d %H:%M:%S") if args.since else None
    until_dt = datetime.strptime(args.until, "%b %d %H:%M:%S") if args.until else None

    extract_logs(args.path, args.keywords, args.output, args.regex, args.exclude, since_dt, until_dt)
