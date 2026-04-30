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

---

#### 3e. Produce Short Clip Package

After writing the script, create a short-clip package for this topic.
Output folder: `short-clip/{topic-slug}/`

**3e-i. Write TTS Script**

Read `scripts/YYYY-MM-DD-{topic-slug}.md` and `wiki/{topic-slug}.md`.
Write a clean spoken-word script in Thai — pure speech only, no section headers, no markdown formatting.

Rules:
- Target length: 60–90 seconds (~150–225 words at Thai speaking pace)
- No labels such as Hook, CTA, เนื้อหาหลัก, etc. — the text flows as one continuous speech
- Keep Thai language throughout; English medical loanwords are fine (same rule as 3d)
- Tone: warm, evidence-based GP speaking directly to a new Thai father
- End naturally (no explicit CTA — keep it for short-form)
- Embed image cue markers inline as `[IMG-01]`, `[IMG-02]` … at natural visual transition points

Filename: `short-clip/{topic-slug}/tts-script.md`

    ---
    title: "{Thai title}"
    type: tts-script
    duration: "60-90s"
    topic_slug: "{topic-slug}"
    source_script: "[[scripts/YYYY-MM-DD-{topic-slug}]]"
    source_wiki: "[[wiki/{topic-slug}]]"
    date: "YYYY-MM-DD"
    ---

    {pure Thai speech — 150-225 words — with [IMG-01] … [IMG-10] cue markers inline}

    ---

    ## Image Cues
    | # | Marker | File | Description |
    |---|--------|------|-------------|
    | 1 | [IMG-01] | 01-{desc}.jpg | {what should be on screen} |
    | 2 | [IMG-02] | 02-{desc}.jpg | … |

    ## Attribution
    | File | Author | License | Source |
    |------|--------|---------|--------|
    | 01-{desc}.jpg | {author} | {CC-BY-SA 4.0 / CC0 / …} | {Wikimedia URL} |

**3e-ii. Find and Download Images**

Search Wikimedia Commons (free public API — no key required):

Step 1 — Search for candidate images (run for each keyword variation):
```
WebFetch: https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={keyword}&srnamespace=6&format=json&srlimit=15
```
Use 2–3 keyword searches in English (e.g. "newborn breastfeeding", "infant latch", "baby sleeping safe").
Collect 15–20 candidate filenames.

Step 2 — Get download URL + license for each candidate:
```
WebFetch: https://commons.wikimedia.org/w/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url|extmetadata&format=json
```
From `extmetadata` extract: `LicenseShortName`, `Artist`, `ObjectName`.
Accept licenses: CC0, CC-BY, CC-BY-SA (any version). Skip: CC-BY-NC, restricted, unknown.

Step 3 — Select 6–10 best images that visually match the video content (variety of scenes).

Step 4 — Download each image:
```bash
curl -L -o "short-clip/{topic-slug}/01-{desc}.jpg" "{image_url}"
```
Name files sequentially: `01-{short-desc}.jpg`, `02-{short-desc}.jpg`, …
Keep description slug short (max 3 words, hyphens, lowercase, English).

If Wikimedia search returns fewer than 6 suitable images, fill remaining slots by recording
the best-match URLs found (don't download) in the Attribution table with note "URL only — verify before use".

Filename: `scripts/YYYY-MM-DD-{topic-slug}.md`

**PERSONA for all scripts:**
- Role: General Practitioner (MD)
- Background: Health Informatics, MBA
- Current job: Data Analyst at a telemedicine company
- Tone: evidence-based, approachable, data-driven
- Language: Thai — English medical loanwords acceptable (Feed, Latch, Colic, SIDS, etc.)
- Target audience: Thai new fathers, baby 0–3 months

**LANGUAGE RULE — คำย่อและศัพท์เทคนิค:**
ทุกครั้งที่ใช้คำย่อ, ศัพท์ทางการแพทย์, หรือ technique เฉพาะทาง ให้ใส่วงเล็บอธิบายเป็นภาษาไทยตามหลังทันที
ตัวอย่าง:
- SIDS (กลุ่มอาการเสียชีวิตกะทันหันในทารก)
- Latch (การอมหัวนมที่ถูกวิธี)
- Colic (อาการร้องไห้ผิดปกติในทารก)
- Jaundice (ภาวะตัวเหลืองในทารกแรกเกิด)
- Tummy time (การฝึกนอนคว่ำเพื่อพัฒนากล้ามเนื้อ)
- AAP (สมาคมกุมารแพทย์อเมริกัน)
- WHO (องค์การอนามัยโลก)
- G6PD (ภาวะพร่องเอนไซม์จีซิกพีดี)
กฎนี้ใช้กับ script เท่านั้น ไม่ใช้กับ wiki (wiki เขียนภาษาอังกฤษ)

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
- Add new short-clip links under `## 🎬 Short Clips` with Thai title and image count
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
    - short-clip: {n} folders ({total images} images downloaded)

    ## Skipped (duplicate)
    - {none, or list topics that were already in wiki/}

    ## Errors
    - {none, or describe any issues}
