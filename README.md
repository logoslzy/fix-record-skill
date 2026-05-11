[中文](#chinese) | [EN](#english)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/claude--code-skill-6e41e2?style=flat-square&logo=claude&logoColor=white&labelColor=1a1a2e">
    <img src="https://img.shields.io/badge/claude--code-skill-6e41e2?style=flat-square&logo=claude&logoColor=white" alt="Claude Code Skill">
  </picture>
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-green?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+">
</p>

<a id="chinese"></a>

# Fix Record

> 结构化记录 Bug 修复过程，并将历史修复经验提炼为可复用知识。

## 为什么

Bug 修复是宝贵的知识。但这些知识常常转瞬即逝: PR 合并后，Slack 讨论被刷走，几周后有人遇到同样的 Bug，却找不到当初的修复记录。

**Fix Record** 通过在仓库中保存结构化修复记录来解决这个问题。每条记录包含 Bug 描述、根因、修复方案、诊断过程和经验教训。配套的 **Record Condense** 技能会定期将所有记录提炼为简明摘要，让 AI 编程助手和团队掌握历史修复、脆弱模块和重复模式的上下文。

## 技能

### 1. `fix-record` - 记录一次 Bug 修复

将当前 Bug 修复保存为带有 frontmatter 元数据的结构化 Markdown 文件。

**触发词:** `fix_record`、`记录修复`、`记录bug`、`记录fix`、`修复记录`、`record this fix`、`save this fix`

**功能:**

- 从对话中提取 Bug 详情，包括症状、根因、修复方案和诊断步骤
- 提示补充关键缺失信息
- 将模板化 Markdown 文件写入 `docs/fix-records/YYYY-MM-DD-<slug>.md`

**Frontmatter 元数据:**

| 字段 | 说明 |
| --- | --- |
| `date` | 修复记录日期 |
| `severity` | `critical` / `high` / `medium` / `low` |
| `status` | `fixed` / `workaround` / `in-progress` |
| `tags` | 用于分组和检索的关键词 |

**记录模板结构:** Bug 描述 -> 根因 -> 修复方案 -> 诊断过程 -> 经验教训

> [!TIP]
> 建议在修复 Bug 后立即使用此技能，趁细节还记忆犹新。

### 2. `record-condense` - 提炼所有修复记录

读取所有历史修复记录，生成一份结构化摘要，涵盖重复模式、高影响修复和脆弱模块。

**触发词:** `record_condense`、`提炼修复`、`condense records`、`汇总修复记录`、`review past fixes`、`summarize fix records`

**功能:**

1. 扫描 `docs/fix-records/` 中的所有修复记录
2. 完整读取每条记录
3. 生成包含五个部分的摘要:
   - **A. 概览**: 总数、日期范围、严重性/状态分布
   - **B. 重复 Bug 模式**: 按标签或根因相似性分组
   - **C. 高影响修复**: `critical` 和 `high` 级别的修复项
   - **D. 修复方案汇总**: 每条修复的一句话摘要
   - **E. 关注清单**: 多次出现在记录中的脆弱文件或模块
4. 将摘要注入当前会话上下文
5. 询问是否保存为永久浓缩记录

**可选辅助脚本:** `scripts/condense.py` 可自动化读取和结构化过程。

```bash
python scripts/condense.py docs/fix-records/
```

## 安装

将本仓库克隆到 Claude Code 技能目录:

```bash
git clone https://github.com/logos-ai/fix-record-skill.git \
  ~/.claude/skills/fix-record-skill
```

然后在项目的 `.claude/settings.json` 中注册技能:

```json
{
  "skills": {
    "fix-record": "~/.claude/skills/fix-record-skill/skills/fix-record/SKILL.md",
    "record-condense": "~/.claude/skills/fix-record-skill/skills/record-condense/SKILL.md"
  }
}
```

## 使用

### 记录一次修复

在 Claude Code 会话中，修复 Bug 后执行:

```text
/fix-record
```

该技能会从对话中提取详情并引导你补充缺失信息。记录会保存到 `docs/fix-records/`。

### 提炼历史记录

查看所有历史修复并获取浓缩摘要:

```text
/record-condense
```

摘要会注入当前会话上下文，也可选择持久化为永久记录。

> [!NOTE]
> 记录以纯 Markdown 文件形式存储在仓库中。将其与代码一起提交，让整个团队都能受益于积累的知识。

## 结构

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

## 许可证

MIT

---

<a id="english"></a>

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

Read all past bug fix records and produce a structured summary covering recurring patterns, high-impact fixes, and fragile areas.

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
5. Asks whether to persist it as a permanent record

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
