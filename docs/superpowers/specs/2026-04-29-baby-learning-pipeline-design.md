# Baby Learning Pipeline — Design Spec
**Date:** 2026-04-29  
**Status:** Approved

---

## Overview

Automated daily pipeline that researches reliable baby care information (0–3 months) for new Thai fathers. Claude Code acts as the AI engine, writing structured notes into an Obsidian vault. A Windows Task Scheduler cron job wakes the computer from Sleep at 06:00 and triggers the pipeline, producing 3 wiki pages + 3 TikTok/YouTube scripts per day.

---

## Goals

- Aggregate evidence-based baby care knowledge from trusted medical sources
- Store structured, interlinked notes in Obsidian (raw → wiki → script)
- Generate 5-minute Thai-language scripts with a consistent doctor persona
- Avoid duplicate topics across runs
- Allow user to pre-queue topics via `inbox.md`; auto-select otherwise
- All settings configurable via `config.yaml` without touching code

---

## Architecture

### Components

| Component | Role |
|---|---|
| **Windows Task Scheduler** | Wakes machine from Sleep at 06:00, runs `run_pipeline.bat` |
| **run_pipeline.bat** | Entry point — calls Claude Code CLI in headless mode |
| **Claude Code CLI** | AI engine: research, synthesize, generate, write |
| **WebSearch (built-in)** | Searches trusted sources for each topic |
| **Obsidian MCP** | Writes/updates all markdown files in the vault |
| **Local Images Plus** | Obsidian plugin — auto-downloads remote images to `assets/` |
| **config.yaml** | Single source of truth for all settings |
| **inbox.md** | User-editable topic queue inside Obsidian |

### Automation: Wake from Sleep (Option A)
- Computer stays in **Sleep mode** (not Shutdown)
- Windows Task Scheduler configured to **wake from sleep** at 06:00
- Pipeline runs, then computer returns to Sleep
- If computer is fully shut down, pipeline does not run that day

---

## Vault Folder Structure

```
Baby_learning/
├── raw/              # Raw clipped notes per topic per source
├── wiki/             # Synthesized wiki pages with backlinks
├── scripts/          # TikTok/YouTube scripts
├── assets/           # Local images (auto-managed by Local Images Plus)
├── logs/             # Daily pipeline run logs
├── docs/             # Specs and planning documents
├── inbox.md          # User topic queue (editable in Obsidian)
├── _index.md         # Master index — auto-updated daily
└── config.yaml       # All pipeline settings
```

---

## Configuration (`config.yaml`)

```yaml
schedule:
  time: "06:00"
  topics_per_day: 3

sources:
  priority:
    - WHO
    - AAP
    - Mayo Clinic
    - NHS
    - PubMed
    - Thai medical guidelines   # กรมอนามัย, แพทยสภา
  min_sources_per_topic: 2

content:
  age_range: "0-3 months"
  language:
    wiki: "english"
    script: "thai"              # Thai with English loanwords allowed
  script_formats:
    rotate: true
    formats: [hook-content-cta, storytelling, qa-mythbusting]

persona:
  role: "General Practitioner"
  background: ["Health Informatics", "MBA", "Data Analyst"]
  company: "Telemedicine"
  tone: "evidence-based, approachable, data-driven"

obsidian:
  vault_path: "C:/Users/wongt/Desktop/Baby_learning"
  folders:
    raw: "raw"
    wiki: "wiki"
    scripts: "scripts"
    assets: "assets"
    logs: "logs"
```

---

## Pipeline Logic (Step-by-Step)

```
STEP 1 — Load & Check
  Read config.yaml
  Read inbox.md → extract Pending topics
  Scan wiki/ → build "done list" for deduplication

STEP 2 — Topic Selection
  If inbox has Pending topics → use those first (up to 3)
  If fewer than 3 → Claude picks remaining topics not in done list
  Update inbox.md: move used topics from Pending → Done

STEP 3 — Research (repeat per topic)
  WebSearch each source per priority order in config
  Collect: URL, key content, image URLs
  Write raw note → MCP → raw/YYYY-MM-DD-topic-source.md

STEP 4 — Wiki Generation (per topic)
  Synthesize all raw notes for the topic
  Cross-link to related existing wiki pages
  Write wiki page → MCP → wiki/topic-slug.md

STEP 5 — Script Generation (per topic)
  Select next format from rotation (hook-content-cta / storytelling / qa-mythbusting)
  Generate Thai-language script using persona from config
  Write script → MCP → scripts/YYYY-MM-DD-topic.md

STEP 6 — Update Index & Log
  Append new wiki + script links to _index.md → MCP
  Write run summary → logs/YYYY-MM-DD.md
```

---

## Note Templates

### Raw Note (`raw/YYYY-MM-DD-topic-source.md`)
```markdown
---
title: "{{topic}}"
type: raw
source_url: "{{url}}"
source_name: "{{WHO|AAP|PubMed|etc}}"
reliability: "high"
date_clipped: "{{YYYY-MM-DD}}"
tags: [{{tags}}]
age_range: "0-3 months"
---

# {{title}} — {{source_name}}

## Key Points
- ...

## Raw Content
{{scraped content}}

## Images
![[assets/{{image-filename}}]]

## Links To
[[wiki/{{topic-slug}}]]
```

### Wiki Page (`wiki/topic-slug.md`)
```markdown
---
title: "{{topic}}"
type: wiki
created: "{{YYYY-MM-DD}}"
last_updated: "{{YYYY-MM-DD}}"
tags: [{{tags}}]
age_range: "0-3 months"
---

# {{title}}

## Summary
{{2-3 sentence synthesis}}

## What Research Says
{{synthesized findings from multiple sources}}

## Practical Guidelines
{{actionable steps for new dads}}

## Thai Context
{{Thai medical guideline notes if applicable}}

## Warning Signs 🚨
{{when to consult a doctor}}

## References
- [[raw/{{source1}}]]
- [[raw/{{source2}}]]

## Related Topics
- [[wiki/{{related1}}]]
- [[wiki/{{related2}}]]
```

### Script (`scripts/YYYY-MM-DD-topic.md`)
```markdown
---
title: "{{Thai title}}"
type: script
format: "{{hook-content-cta|storytelling|qa-mythbusting}}"
duration: "5 min"
platform: [TikTok, YouTube]
date: "{{YYYY-MM-DD}}"
source_wiki: "[[wiki/{{topic-slug}}]]"
status: ready
---

# 🎬 HOOK (0–5 วินาที)
{{hook}}

# 📖 เนื้อหาหลัก (~4 นาที)
{{main content in Thai, English loanwords ok}}

# 📢 CTA (30 วินาที)
{{call to action}}

## Speaker Notes
{{additional context for the doctor speaker}}
```

### Master Index (`_index.md`)
```markdown
# 📚 Baby Learning Index

## 🗂 Wiki Topics
### Sleep & Rest
- [[wiki/newborn-sleep-patterns]] — Newborn Sleep Patterns

### Feeding
- [[wiki/breastfeeding-basics]] — Breastfeeding Basics

## 🎬 Scripts
- [[scripts/2026-04-30-newborn-sleep]] — ทารกนอนวันละกี่ชั่วโมง?

_Last updated: {{YYYY-MM-DD HH:MM}}_
```

### Log (`logs/YYYY-MM-DD.md`)
```markdown
# Pipeline Run — {{YYYY-MM-DD HH:MM}}

## Topics Processed
1. ✅ {{topic 1}} ({{n}} sources)
2. ✅ {{topic 2}} ({{n}} sources)
3. ✅ {{topic 3}} ({{n}} sources)

## Files Created
- raw: {{n}} files
- wiki: {{n}} files
- scripts: {{n}} files

## Skipped (duplicate)
- {{any skipped topics}}

## Errors
- {{none|error details}}
```

---

## Inbox (`inbox.md`)

User-editable file inside Obsidian. Pipeline reads this on every run.

```markdown
## Pending Topics
- การอาบน้ำทารกแรกเกิดที่ถูกวิธี
- วิธีรับมือ colic

## Done (auto-moved by pipeline)
- ~~Newborn sleep patterns~~
```

---

## Image Handling

- Pipeline saves raw markdown with original remote image URLs
- **Local Images Plus** (Obsidian plugin) automatically detects remote URLs, downloads images to `assets/`, and rewrites links in-place
- No image download logic needed in the pipeline itself

---

## Speaker Persona

Used in all script generation prompts:

- **Role:** General Practitioner (MD)
- **Background:** Health Informatics, MBA, Data Analyst
- **Current role:** Data Analyst at a telemedicine company
- **Tone:** Evidence-based, approachable, data-driven
- **Language:** Thai with English medical loanwords acceptable
- **Angle:** Bridges clinical evidence + data insight + real-world parenting context

---

## Content Sources (Priority Order)

1. WHO
2. AAP (American Academy of Pediatrics)
3. Mayo Clinic
4. NHS
5. PubMed / Google Scholar (academic papers)
6. Thai medical guidelines — กรมอนามัย, แพทยสภา, โรงพยาบาลศิริราช etc.

Minimum 2 sources required per topic before wiki generation proceeds.

---

## Script Format Rotation

| Format | Style |
|---|---|
| `hook-content-cta` | TikTok-style: strong hook → evidence → call to action |
| `storytelling` | "พ่อมือใหม่หลายคนไม่รู้ว่า..." narrative → knowledge |
| `qa-mythbusting` | Common question/myth → medical answer with data |

Formats rotate automatically. Configurable in `config.yaml`.

---

## Setup Checklist (One-time)

1. Install Obsidian → open `Baby_learning/` as vault
2. Install **Local Images Plus** plugin in Obsidian
3. Install **Obsidian MCP** and connect to Claude Code
4. Configure `config.yaml` with correct vault path
5. Set up Windows Task Scheduler:
   - Trigger: Daily at 06:00, **enable "Wake the computer to run this task"**
   - Action: run `run_pipeline.bat`
6. Test with manual run before enabling schedule

---

## Future Considerations

- If daily usage hits Claude Pro limits → reduce `topics_per_day` to 2 in config
- If cloud automation needed later → migrate to VPS + Claude API (~$3–5/month for this volume)
- Obsidian Web Clipper can supplement pipeline for manual one-off clipping to `raw/`
