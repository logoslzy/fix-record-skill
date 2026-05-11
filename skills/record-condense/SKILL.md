---
name: record-condense
description: |
  Condense all past bug fix records into a summary and inject it into context.
  Use this skill ONLY when the user wants to review, condense, or summarize
  past fix records — NOT when they want to save a new fix record.
  
  Trigger phrases: "record_condense", "提炼修复", "condense records",
  "汇总修复记录", "review past fixes", "summarize fix records"
  
  Do NOT trigger for: "fix_record", "记录修复", "记录bug", "记录fix",
  "修复记录", "record this fix", or any request to save/discuss a new bug fix.
---

# Record Condense

## Overview

Read ALL fix records from `docs/fix-records/`, produce a condensed summary,
inject it into the current context, and ask the user whether to save permanently.

The condensed summary is always injected into context so the AI can reference
past fixes during this session. Persisting the file to disk is optional and
decided by the user after reading the summary.

---

## Workflow

### Step 1: Locate records

Scan `./docs/fix-records/` for all `.md` files. Skip any named
`CONDENSED.md` or `.CONDENSED.tmp.md`. If the directory doesn't exist or is empty,
tell the user there are no records yet and stop.

### Step 2: Read every record

Read the full content of each fix record file. Do not skip any.

### Step 3: Produce the condensed summary

Analyze all records and produce a structured summary with these five sections:

**A. Overview**
- Total number of fixes recorded
- Date range (earliest to latest)
- Severity breakdown (critical/high/medium/low counts)
- Status breakdown (fixed/workaround/in-progress counts)

**B. Recurring Bug Patterns**
- Group similar bugs by tags, affected modules, or root cause similarity
- For each pattern: how many occurrences, what files/modules are affected,
  what the common root cause is

**C. High-Impact Fixes**
- List critical and high severity fixes with one-line summaries
- Note what made each one high-impact

**D. Common Solutions Catalog**
- What fix approaches appear across multiple records?
- Which solutions have proven most reliable?

**E. Watch List**
- Files or modules mentioned in multiple bug records — these are fragile areas
- Anti-patterns that have caused multiple bugs

### Step 4: Write to temp file

Save the summary as `docs/fix-records/.CONDENSED.tmp.md`. This is a temporary
file — NOT a permanent record yet.

### Step 5: Inject into context

Read the temp file back and present the full summary to the user. This is the
critical step — the summary must enter the AI's context so future fixes in
this session can reference it.

### Step 6: Ask whether to save permanently

After presenting the summary, ask:

> Save this condensed summary as a permanent record? (yes/no)

- **If YES**: Promote the temp file to a permanent record. Add frontmatter:

  ```markdown
  ---
  date: YYYY-MM-DD
  severity: low
  status: fixed
  tags: [condensed-summary, batch-condense]
  ---
  ```

  Save as `docs/fix-records/YYYY-MM-DD-condensed-summary-N.md` where N is
  auto-incremented (01, 02, ...). Confirm the save path to the user.

- **If NO**: Delete `.CONDENSED.tmp.md` immediately. The summary has already
  been injected into context, so it benefits this session regardless.

**Important**: Always ask. Never skip the save/discard decision.

---

## The condense script (optional helper)

A Python script is available at `scripts/condense.py` relative to this
SKILL.md. It can be used to automate the reading and structuring step.
Usage: `python scripts/condense.py <records_dir>`
