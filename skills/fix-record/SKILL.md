---
name: fix-record
description: |
  Record a bug fix as a structured document. Use this skill ONLY when the user
  explicitly wants to save or record a bug fix — NOT when they want to review
  or condense past records.
  
  Trigger phrases: "fix_record", "记录修复", "记录bug", "记录fix",
  "修复记录", "record this fix", "save this fix"
  
  Do NOT trigger for: "record_condense", "提炼修复", "condense records",
  "汇总修复记录", or any request to review/condense existing records.
---

# Fix Record

## Overview

Save the current bug fix as a structured markdown record in the project's
`docs/fix-records/` directory.

---

## Workflow

1. **Determine the record directory.** Default: `./docs/fix-records/` relative
   to the project root. Create the directory if it doesn't exist.

2. **Gather information from the conversation.** Extract from recent history:
   - What was the bug? (symptoms, error messages, unexpected behavior)
   - What was the root cause?
   - What was the fix?
   - What was the diagnostic process?
   - Any lessons learned or things to watch for in the future

3. **Ask the user to fill gaps.** If any of the above is missing, ask briefly.
   Don't be exhaustive — just cover the most important missing pieces.

4. **Generate the record file.** Use this exact template:

```markdown
---
date: YYYY-MM-DD
severity: critical | high | medium | low
status: fixed | workaround | in-progress
tags: [tag1, tag2]
---

# [Bug Title - One line summary]

## Bug Description
[What was the bug? What were the symptoms?]

## Root Cause
[What specifically caused the bug? Which file/function/logic was faulty?]

## Fix
[What code or config change resolved it? Be specific — include file paths.]

## Diagnostic Process
[Step-by-step: how was the bug found and traced to its root cause?]

## Lessons Learned
[What patterns should be watched for? Any preventative measures?]
```

5. **Write the file.** Name it `YYYY-MM-DD-<short-slug>.md` (e.g.,
   `2026-05-11-null-pointer-auth-middleware.md`). Place it in the records directory.

6. **Confirm to the user** where the file was saved, with a 1-line summary.
