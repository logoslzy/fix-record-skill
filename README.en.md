[中文](./README.md) | [EN](./README.en.md)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/claude--code-skill-6e41e2?style=flat-square&logo=claude&logoColor=white&labelColor=1a1a2e">
    <img src="https://img.shields.io/badge/claude--code-skill-6e41e2?style=flat-square&logo=claude&logoColor=white" alt="Claude Code Skill">
  </picture>
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-green?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+">
</p>

# Fix Record

> Capture bug fixes in a structured format and condense past fixes into reusable knowledge.

## Why

Bug fixes are knowledge. But too often, that knowledge evaporates: the PR gets merged, the Slack thread scrolls away, and a few weeks later someone hits the same bug with no trace of the original fix.

**Fix Record** solves this by storing structured fix records directly in your repository. Each record documents the bug, root cause, fix, diagnostic process, and lessons learned. The companion **Record Condense** skill periodically summarizes all records so your AI coding agent and team retain context about past fixes, fragile areas, and recurring patterns.

## Skills

### 1. `fix-record` - Record a Bug Fix

Save the current bug fix as a structured Markdown record with frontmatter metadata.

**Trigger phrases:** `fix_record`, `记录修复`, `记录bug`, `记录fix`, `修复记录`, `record this fix`, `save this fix`

**What it does:**

- Extracts bug details from the conversation, including symptoms, root cause, fix, and diagnostic steps
- Prompts you to fill any critical gaps
- Writes a templated Markdown file to `docs/fix-records/YYYY-MM-DD-<slug>.md`

**Frontmatter metadata:**

| Field | Description |
| --- | --- |
| `date` | When the fix was recorded |
| `severity` | `critical` / `high` / `medium` / `low` |
| `status` | `fixed` / `workaround` / `in-progress` |
| `tags` | Keywords for grouping and search |

**Record template sections:** Bug Description -> Root Cause -> Fix -> Diagnostic Process -> Lessons Learned

> [!TIP]
> Use this skill immediately after fixing a bug while the details are still fresh.

### 2. `record-condense` - Condense All Fix Records

Read all past fix records and produce a structured summary covering recurring patterns, high-impact fixes, and fragile areas.

**Trigger phrases:** `record_condense`, `提炼修复`, `condense records`, `汇总修复记录`, `review past fixes`, `summarize fix records`

**What it does:**

1. Scans `docs/fix-records/` for all fix records
2. Reads every record in full
3. Generates a summary with five sections:
   - **A. Overview**: totals, date range, severity and status breakdown
   - **B. Recurring Bug Patterns**: grouped by tags or root cause similarity
   - **C. High-Impact Fixes**: `critical` and `high` severity items
   - **D. Fix Summary**: one-line summaries of each fix
   - **E. Watch List**: fragile files or modules mentioned in multiple records
4. Injects the summary into the current session context
5. Asks whether to persist it as a permanent condensed record

**Optional helper script:** `scripts/condense.py` automates the reading and structuring step.

```bash
python scripts/condense.py docs/fix-records/
```

## Installation

Clone this repository into your Claude Code skills directory:

```bash
git clone https://github.com/logos-ai/fix-record-skill.git \
  ~/.claude/skills/fix-record-skill
```

Then register the skills in your project's `.claude/settings.json`:

```json
{
  "skills": {
    "fix-record": "~/.claude/skills/fix-record-skill/skills/fix-record/SKILL.md",
    "record-condense": "~/.claude/skills/fix-record-skill/skills/record-condense/SKILL.md"
  }
}
```

## Usage

### Record a fix

In a Claude Code session, after fixing a bug, run:

```text
/fix-record
```

The skill extracts details from the conversation and guides you through filling any missing information. The record is saved to `docs/fix-records/`.

### Condense past records

To review all past fixes and get a condensed summary:

```text
/record-condense
```

The summary is injected into your session context and can also be saved as a permanent record.

> [!NOTE]
> Records are stored as plain Markdown files in your repository. Commit them alongside your code so the whole team benefits from the accumulated knowledge.

## Structure

```text
├── skills/
│   ├── fix-record/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── template.md
│   └── record-condense/
│       ├── SKILL.md
│       └── scripts/
│           └── condense.py
├── README.md
└── README.en.md
```

## License

MIT
