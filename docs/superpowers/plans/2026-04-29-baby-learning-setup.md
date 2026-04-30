# Baby Learning Pipeline — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up a fully automated daily pipeline that researches baby care topics (0–3 months), writes structured Obsidian notes, and generates Thai TikTok/YouTube scripts — running every morning at 06:00 via Windows Task Scheduler.

**Architecture:** Claude Code CLI runs headlessly via `run_pipeline.bat`, reads `CLAUDE.md` for pipeline instructions, uses built-in WebSearch + filesystem tools to write markdown directly to the Obsidian vault. No Claude API needed — uses Claude Pro subscription via stored OAuth token.

**Tech Stack:** Obsidian, Claude Code CLI, Windows Task Scheduler, Markdown, YAML

---

## File Map

| File | Purpose |
|---|---|
| `CLAUDE.md` | Pipeline instructions — Claude Code reads this automatically on launch |
| `config.yaml` | All settings (schedule, sources, persona, formats) |
| `inbox.md` | User topic queue — edit in Obsidian to pre-queue topics |
| `_index.md` | Master index — auto-updated by pipeline each run |
| `run_pipeline.bat` | Windows entry point called by Task Scheduler |
| `raw/` | Raw research notes per source per topic |
| `wiki/` | Synthesized wiki pages with cross-links |
| `scripts/` | Thai TikTok/YouTube scripts |
| `assets/` | Local images (auto-managed by Local Images Plus plugin) |
| `logs/` | Daily run summaries |

---

### Task 1: Install Obsidian and Open Vault

**Files:** None (installation)

- [ ] **Step 1: Download Obsidian**

  Open browser → go to `https://obsidian.md` → click Download → choose Windows (.exe)

- [ ] **Step 2: Install Obsidian**

  Run the downloaded `.exe` installer → accept defaults → finish

- [ ] **Step 3: Open Baby_learning as vault**

  - Launch Obsidian
  - On the welcome screen click **"Open folder as vault"**
  - Navigate to `C:\Users\wongt\Desktop\Baby_learning`
  - Click **Select Folder**
  - If prompted "Trust author" → click **Trust and Enable**

- [ ] **Step 4: Verify**

  Obsidian opens and the left sidebar shows the folder. You should see `CLAUDE.md` and the `docs/` folder already there.

---

### Task 2: Install Local Images Plus Plugin

**Files:** None (Obsidian plugin)

- [ ] **Step 1: Open settings**

  In Obsidian press `Ctrl+,` to open Settings

- [ ] **Step 2: Enable community plugins**

  - Go to **Community plugins** in left sidebar
  - Click **Turn on community plugins** → confirm

- [ ] **Step 3: Install Local Images Plus**

  - Click **Browse**
  - Search: `Local Images Plus`
  - Click **Install** → then **Enable**

- [ ] **Step 4: Configure download folder**

  - Click the gear icon next to Local Images Plus
  - Set **"Media folder"** to `assets`
  - Leave other settings as default

- [ ] **Step 5: Verify**

  Settings → Community plugins → Local Images Plus shows as **Enabled** (toggle is blue)

---

### Task 3: Create Vault Folder Structure

**Files:** Create `raw/`, `wiki/`, `scripts/`, `assets/`, `logs/`

- [ ] **Step 1: Open terminal**

  Press `Win+R` → type `cmd` → Enter

- [ ] **Step 2: Create all folders**

  ```bat
  mkdir "C:\Users\wongt\Desktop\Baby_learning\raw"
  mkdir "C:\Users\wongt\Desktop\Baby_learning\wiki"
  mkdir "C:\Users\wongt\Desktop\Baby_learning\scripts"
  mkdir "C:\Users\wongt\Desktop\Baby_learning\assets"
  mkdir "C:\Users\wongt\Desktop\Baby_learning\logs"
  ```

- [ ] **Step 3: Verify in Obsidian**

  In Obsidian left sidebar click the folder icon — you should see all 5 folders: `assets`, `logs`, `raw`, `scripts`, `wiki`

---

### Task 4: Create config.yaml

**Files:** Create `C:\Users\wongt\Desktop\Baby_learning\config.yaml`

- [ ] **Step 1: Create config.yaml**

  Create the file with this exact content:

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
      - Thai medical guidelines
    min_sources_per_topic: 2

  content:
    age_range: "0-3 months"
    language:
      wiki: "english"
      script: "thai"
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
  ```

- [ ] **Step 2: Verify**

  Open `config.yaml` in Obsidian — displays as readable text with all sections visible

---

### Task 5: Create inbox.md

**Files:** Create `C:\Users\wongt\Desktop\Baby_learning\inbox.md`

- [ ] **Step 1: Create inbox.md**

  ```markdown
  # 📥 Topic Inbox

  Add topics here before each run. Pipeline processes **Pending Topics** first.
  If Pending is empty, Claude auto-selects topics not already in `wiki/`.

  ## Pending Topics
  <!-- Add topics below, one per line starting with -  -->
  <!-- Example: - วิธีรับมือ colic ในทารกแรกเกิด       -->

  ## Done
  <!-- Pipeline auto-moves completed topics here -->
  ```

- [ ] **Step 2: Verify**

  Open `inbox.md` in Obsidian — shows both sections cleanly. You can edit the Pending section to add your first topics.

---

### Task 6: Create _index.md

**Files:** Create `C:\Users\wongt\Desktop\Baby_learning\_index.md`

- [ ] **Step 1: Create _index.md**

  ```markdown
  # 📚 Baby Learning — Master Index

  > Auto-updated by pipeline each run. Do not edit manually.

  ## 🗂 Wiki Topics

  *(No topics yet — run the pipeline to populate)*

  ## 🎬 Scripts

  *(No scripts yet — run the pipeline to populate)*

  ---
  _Last updated: (pipeline not yet run)_
  ```

---

### Task 7: Update CLAUDE.md with Full Pipeline Instructions

**Files:** Replace `C:\Users\wongt\Desktop\Baby_learning\CLAUDE.md`

This is the most critical file. Claude Code reads `CLAUDE.md` automatically when launched from the vault directory — this is how it knows what to do.

- [ ] **Step 1: Replace CLAUDE.md with pipeline instructions**

  Replace the current minimal `CLAUDE.md` with:

  ```markdown
  # CLAUDE.md

  This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

  ## Project

  Automated daily pipeline: research baby care topics (0–3 months) for new Thai fathers →
  write structured Obsidian notes → generate Thai TikTok/YouTube scripts.

  Vault path: C:/Users/wongt/Desktop/Baby_learning

  ## Executing the Pipeline

  When asked to "execute the baby learning pipeline", complete all 5 steps below in order.
  Do not stop until all steps are done for all topics.

  ---

  ### STEP 1: Load and Check

  1. Read `config.yaml` — note topics_per_day, sources, persona settings
  2. Read `inbox.md` — extract all bullet items under `## Pending Topics`
  3. List all files in `wiki/` — build a deduplication list of already-covered topics

  ---

  ### STEP 2: Topic Selection

  - Use Pending Topics from `inbox.md` first (up to `topics_per_day` count)
  - If inbox has fewer topics than needed, generate additional baby care (0–3 months)
    topics that do NOT appear in the wiki/ deduplication list
  - Update `inbox.md`:
    - Remove used topics from `## Pending Topics`
    - Add them to `## Done` as strikethrough: `~~topic name~~`

  ---

  ### STEP 3: For Each Topic — Research, Raw, Wiki, Script

  Repeat the following for EACH selected topic:

  #### 3a. Research

  Use WebSearch to find content from these sources in priority order:
  WHO → AAP (American Academy of Pediatrics) → Mayo Clinic → NHS → PubMed → Thai medical guidelines (กรมอนามัย, แพทยสภา, Siriraj guidelines)

  Find at least 2 reliable sources. For each source collect:
  - Page URL
  - Key findings and evidence
  - Any image URLs in the content

  #### 3b. Write Raw Note (one file per source)

  Filename: `raw/YYYY-MM-DD-{topic-slug}-{source-name}.md`

  Front matter + content structure:

      ---
      title: "{topic}"
      type: raw
      source_url: "{url}"
      source_name: "{source}"
      reliability: "high"
      date_clipped: "YYYY-MM-DD"
      tags: [{relevant tags}]
      age_range: "0-3 months"
      ---

      # {title} — {source_name}

      ## Key Points
      - {bullet points of key findings}

      ## Raw Content
      {detailed content from the source}

      ## Images
      {if images found: ![description](url)}

      ## Links To
      [[wiki/{topic-slug}]]

  #### 3c. Write Wiki Page

  Synthesize ALL raw notes for this topic into one wiki page.
  Cross-link to related existing wiki pages using [[wiki/...]] syntax.

  Filename: `wiki/{topic-slug}.md`

      ---
      title: "{topic in English}"
      type: wiki
      created: "YYYY-MM-DD"
      last_updated: "YYYY-MM-DD"
      tags: [{tags}]
      age_range: "0-3 months"
      ---

      # {Topic Title}

      ## Summary
      {2-3 sentences synthesis in English}

      ## What Research Says
      {synthesized findings from all sources, cite inline}

      ## Practical Guidelines
      {actionable steps written for new dads}

      ## Thai Context
      {Thai guideline notes if found — omit section if none}

      ## Warning Signs 🚨
      {list of symptoms/situations requiring a doctor}

      ## References
      - [[raw/{raw-note-filename-1}]]
      - [[raw/{raw-note-filename-2}]]

      ## Related Topics
      - [[wiki/{related-topic-slug}]]

  #### 3d. Write Script

  Check the most recent files in `scripts/` to see which format was last used.
  Rotate to the next format in this cycle:
  hook-content-cta → storytelling → qa-mythbusting → hook-content-cta → ...

  Filename: `scripts/YYYY-MM-DD-{topic-slug}.md`

  Use the PERSONA below for all scripts.

  **PERSONA:**
  - Role: General Practitioner (MD)
  - Background: Health Informatics, MBA
  - Current job: Data Analyst at a telemedicine company
  - Tone: evidence-based, approachable, data-driven
  - Language: Thai — English medical loanwords acceptable (e.g., Feed, Latch, Colic, SIDS)
  - Target audience: Thai new fathers, baby 0–3 months

  **FORMAT STYLES:**

  `hook-content-cta` — TikTok style:
  - Hook: strong opening statement or surprising fact (0–5 sec)
  - Content: evidence + practical advice (4 min)
  - CTA: follow for more / save this video (30 sec)

  `storytelling` — Narrative style:
  - Open with "พ่อมือใหม่หลายคนไม่รู้ว่า..." or similar relatable scenario
  - Weave medical knowledge into the story
  - End with key takeaway

  `qa-mythbusting` — Q&A style:
  - Start with a common myth or question Thai parents ask
  - Answer with medical evidence + data
  - End with practical guidance

  Script file structure:

      ---
      title: "{Thai title}"
      type: script
      format: "{hook-content-cta | storytelling | qa-mythbusting}"
      duration: "5 min"
      platform: [TikTok, YouTube]
      date: "YYYY-MM-DD"
      source_wiki: "[[wiki/{topic-slug}]]"
      status: ready
      ---

      # 🎬 HOOK (0–5 วินาที)
      {hook text in Thai}

      # 📖 เนื้อหาหลัก (~4 นาที)
      {main content in Thai, can include English loanwords}

      # 📢 CTA (30 วินาที)
      {call to action in Thai}

      ## Speaker Notes
      {extra context or stats the doctor speaker should know}

  ---

  ### STEP 4: Update Master Index

  Edit `_index.md`:
  - Add new wiki links under `## 🗂 Wiki Topics`, organized by category
    (categories: Sleep & Rest, Feeding, Development, Health & Safety, Hygiene)
  - Add new script links under `## 🎬 Scripts` with Thai title
  - Update the "Last updated" timestamp at the bottom

  ---

  ### STEP 5: Write Run Log

  Create `logs/YYYY-MM-DD.md`:

      # Pipeline Run — YYYY-MM-DD HH:MM

      ## Topics Processed
      1. ✅ {topic 1} ({n} sources)
      2. ✅ {topic 2} ({n} sources)
      3. ✅ {topic 3} ({n} sources)

      ## Files Created
      - raw: {n} files
      - wiki: {n} files
      - scripts: {n} files

      ## Skipped (duplicate)
      - {none, or list topics that were already in wiki/}

      ## Errors
      - {none, or describe any issues}
  ```

- [ ] **Step 2: Verify**

  Open `CLAUDE.md` in Obsidian — all 5 pipeline steps are visible and readable

---

### Task 8: Create run_pipeline.bat

**Files:** Create `C:\Users\wongt\Desktop\Baby_learning\run_pipeline.bat`

- [ ] **Step 1: Create run_pipeline.bat**

  ```bat
  @echo off
  cd /d "C:\Users\wongt\Desktop\Baby_learning"
  echo [%date% %time%] Baby Learning Pipeline starting...
  claude --dangerously-skip-permissions -p "Execute the baby learning pipeline as described in CLAUDE.md. Complete all 5 steps for all topics. Do not stop early."
  echo [%date% %time%] Pipeline finished.
  pause
  ```

  The `pause` at the end keeps the window open so you can see results on manual runs. Remove it later once you're confident the pipeline works.

- [ ] **Step 2: Do a manual test run**

  Double-click `run_pipeline.bat`

  Expected behavior:
  - Terminal window opens
  - Claude Code starts running
  - You see it reading config.yaml, selecting topics, searching the web
  - Files appear in `raw/`, `wiki/`, `scripts/`
  - Window says "Pipeline finished."

- [ ] **Step 3: Verify output in Obsidian**

  In Obsidian check:
  - `raw/` — at least 6 files (2+ sources × 3 topics)
  - `wiki/` — 3 files with cross-links
  - `scripts/` — 3 files in Thai
  - `_index.md` — updated with new links
  - `logs/` — one log file for today

  If any step failed, read the log file for details.

---

### Task 9: Set Up Windows Task Scheduler

**Files:** None (Windows configuration)

- [ ] **Step 1: Open Task Scheduler**

  Press `Win+R` → type `taskschd.msc` → press Enter

- [ ] **Step 2: Create new task (not Basic Task)**

  In the right panel click **"Create Task..."** (not "Create Basic Task")

- [ ] **Step 3: General tab**

  - Name: `Baby Learning Pipeline`
  - Leave "Run only when user is logged on" selected (default)
  - Check **"Run with highest privileges"**

- [ ] **Step 4: Triggers tab — add schedule**

  - Click **New**
  - Begin task: `On a schedule`
  - Settings: `Daily`
  - Start: today's date, time: `06:00:00`
  - Recur every: `1` days
  - Check **Enabled**
  - Click OK

- [ ] **Step 5: Actions tab — point to bat file**

  - Click **New**
  - Action: `Start a program`
  - Program/script: `C:\Users\wongt\Desktop\Baby_learning\run_pipeline.bat`
  - Start in: `C:\Users\wongt\Desktop\Baby_learning`
  - Click OK

- [ ] **Step 6: Conditions tab — enable wake from sleep**

  - Check **"Wake the computer to run this task"** ← this is the critical setting
  - If on a laptop: uncheck "Start the task only if the computer is on AC power"

- [ ] **Step 7: Settings tab**

  - Check "If the task fails, restart every: 1 hour" — Attempt restart up to 2 times
  - Click OK
  - Enter your Windows password if prompted

- [ ] **Step 8: Verify task was created**

  Find "Baby Learning Pipeline" in the task list.
  Right-click → **Run** to trigger it immediately.
  Expected: `run_pipeline.bat` window opens and pipeline runs.

---

### Task 10: Configure Sleep Mode (Not Shutdown)

**Files:** None (Windows settings)

- [ ] **Step 1: Set default power action to Sleep**

  - Press `Win+I` → System → Power & Sleep
  - Under "Sleep" — set both "On battery" and "Plugged in" to a value (e.g., Never, or 30 min)
  - Important: use **Sleep** not **Hibernate** for fastest wake

- [ ] **Step 2: Test wake-from-sleep**

  - Temporarily set the Task Scheduler trigger to 2 minutes from now
  - Put computer to Sleep manually: Start → Power → Sleep
  - Wait — computer should wake up, run the pipeline, then you can sleep it again
  - Reset trigger back to `06:00:00`

- [ ] **Step 3: Daily habit**

  Instead of shutting down at night: Start → Power → **Sleep**
  Pipeline runs at 06:00, new content is ready when you wake up.

---

## Note on Obsidian MCP

The design spec listed Obsidian MCP as a component. This plan intentionally skips it for the initial setup — Claude Code's built-in filesystem tools (Read/Write) write markdown directly to the vault folder, which Obsidian picks up automatically. This is simpler and has zero additional setup.

MCP can be added later if you want tighter Obsidian integration (e.g., triggering vault index refresh programmatically). It is not required for the pipeline to work.

---

## Setup Complete ✅

After all tasks are done, your daily workflow is:

1. **Before bed (optional):** Open `inbox.md` in Obsidian, add topics you want researched
2. **Put computer to Sleep** (not shutdown)
3. **Wake up** — 3 new wiki pages + 3 scripts are ready in Obsidian
4. **Review scripts** in `scripts/` → record your TikTok/YouTube content

To change the number of daily scripts: edit `config.yaml` → change `topics_per_day`
To change the schedule: update the trigger in Windows Task Scheduler
