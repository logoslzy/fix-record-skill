#!/usr/bin/env python3
"""
Condense fix records from a directory into a structured summary.

Usage:
    python condense.py <records_dir> [--output <output_path>]

Reads all .md files (except .CONDENSED.tmp.md and CONDENSED.md) from the
records directory, extracts structured data, and produces a condensed summary.

The summary is a temporary artifact by default — the caller decides whether to
persist it as a permanent record or delete it after injecting it into context.
"""

import os
import re
import sys
from datetime import datetime
from collections import Counter, defaultdict

def parse_frontmatter(content):
    """Extract YAML-like frontmatter fields from markdown content."""
    fields = {}
    lines = content.split("\n")
    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue
        if in_frontmatter:
            match = re.match(r"(\w+):\s*(.+)", line)
            if match:
                key, value = match.groups()
                value = value.strip()
                if key == "tags":
                    value = [t.strip() for t in value.strip("[]").split(",") if t.strip()]
                fields[key] = value
    return fields

def parse_sections(content):
    """Extract sections from markdown content."""
    sections = {}
    # Split on ## headers
    parts = re.split(r"\n## ", content)
    for part in parts[1:]:  # skip frontmatter
        match = re.match(r"([^\n]+)\n(.+)", part, re.DOTALL)
        if match:
            title = match.group(1).strip()
            body = match.group(2).strip()
            sections[title] = body
    return sections

def extract_title(content):
    """Extract the # title from content."""
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"

def condense(records_dir):
    """Read all records and produce a condensed summary."""
    records = []
    for fname in sorted(os.listdir(records_dir)):
        if not fname.endswith(".md") or fname in ("CONDENSED.md", ".CONDENSED.tmp.md"):
            continue
        fpath = os.path.join(records_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        fm = parse_frontmatter(content)
        sections = parse_sections(content)
        title = extract_title(content)
        records.append({
            "file": fname,
            "title": title,
            "frontmatter": fm,
            "sections": sections,
        })

    if not records:
        return "No fix records found."

    # --- A. Overview ---
    severities = Counter()
    statuses = Counter()
    all_tags = Counter()
    dates = []

    for r in records:
        fm = r["frontmatter"]
        severities[fm.get("severity", "unknown")] += 1
        statuses[fm.get("status", "unknown")] += 1
        for tag in fm.get("tags", []):
            all_tags[tag] += 1
        if "date" in fm:
            dates.append(fm["date"])

    dates.sort()
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "unknown"

    overview = f"""## A. Overview
- **Total records**: {len(records)}
- **Date range**: {date_range}
- **Severity**: {dict(severities)}
- **Status**: {dict(statuses)}
"""

    # --- B. Recurring Patterns ---
    tag_groups = defaultdict(list)
    for r in records:
        for tag in r["frontmatter"].get("tags", []):
            tag_groups[tag].append(r["title"])

    patterns_lines = []
    if tag_groups:
        patterns_lines.append("## B. Recurring Bug Patterns")
        for tag, titles in sorted(tag_groups.items(), key=lambda x: -len(x[1])):
            if len(titles) >= 2:
                patterns_lines.append(f"\n### {tag} ({len(titles)} occurrences)")
                for t in titles:
                    patterns_lines.append(f"- {t}")

    # --- C. High-Impact Fixes ---
    high_impact = [r for r in records if r["frontmatter"].get("severity") in ("critical", "high")]
    impact_lines = ["## C. High-Impact Fixes"]
    if high_impact:
        for r in high_impact:
            sev = r["frontmatter"].get("severity", "")
            impact_lines.append(f"- [{sev.upper()}] {r['title']}")
    else:
        impact_lines.append("No critical or high severity fixes recorded.")

    # --- D. Common Solutions ---
    fix_summaries = []
    for r in records:
        if "Fix" in r["sections"]:
            fix_text = r["sections"]["Fix"]
            # Truncate to first 2 sentences
            sentences = re.split(r"(?<=[.!?])\s+", fix_text)
            short = " ".join(sentences[:2])
            fix_summaries.append(f"- **{r['title']}**: {short}")

    solutions_lines = ["## D. Fix Summary"]
    solutions_lines.extend(fix_summaries)

    # --- E. Watch List ---
    # Look for file paths mentioned in Root Cause or Fix sections
    file_mentions = Counter()
    for r in records:
        for section_name in ("Root Cause", "Fix"):
            if section_name in r["sections"]:
                # Find file paths like src/foo/bar.ts or path/to/file.py
                paths = re.findall(r"`?([\w./-]+\.[a-z]{1,6})`?", r["sections"][section_name])
                for p in paths:
                    if "/" in p or "\\" in p:  # likely a file path
                        file_mentions[p] += 1

    watch_lines = ["## E. Watch List (Fragile Areas)"]
    if file_mentions:
        for path, count in file_mentions.most_common(10):
            watch_lines.append(f"- `{path}` — mentioned in {count} fix record(s)")
    else:
        watch_lines.append("No specific files identified as fragile areas yet.")

    # --- Assemble ---
    return "\n\n".join([
        f"# Fix Records Condensed Summary\n",
        overview,
        "\n".join(patterns_lines) if patterns_lines else "## B. Recurring Bug Patterns\nNone identified yet.",
        "\n".join(impact_lines),
        "\n".join(solutions_lines),
        "\n".join(watch_lines),
    ])


def main():
    if len(sys.argv) < 2:
        print("Usage: python condense.py <records_dir> [--output <output_path>]")
        sys.exit(1)

    records_dir = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    if not os.path.isdir(records_dir):
        print(f"Error: {records_dir} is not a directory or doesn't exist.")
        sys.exit(1)

    summary = condense(records_dir)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Condensed summary written to {output_path}")
    else:
        print(summary)


if __name__ == "__main__":
    main()
