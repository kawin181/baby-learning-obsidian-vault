# Save — Baby Learning Pipeline Session Log

บันทึกสิ่งที่ทำไปแล้วและการตั้งค่าทั้งหมด เพื่อใช้อ้างอิงในครั้งต่อไป

---

## สิ่งที่สร้างไปแล้ว (ณ 2026-04-30)

### ไฟล์หลักในระบบ

| ไฟล์ | หน้าที่ |
|---|---|
| `CLAUDE.md` | instructions ให้ Claude Code รัน pipeline ทั้ง 5 step |
| `config.yaml` | ตั้งค่าทั้งหมด (เวลา, จำนวน script, sources, persona) |
| `inbox.md` | ใส่ topic ที่อยากรู้ไว้ล่วงหน้า pipeline หยิบก่อน |
| `_index.md` | master index รวม link wiki และ script ทั้งหมด |
| `run_pipeline.bat` | entry point — double-click หรือ Task Scheduler รัน |
| `generate_tts.py` | แปลง script เป็นไฟล์เสียง MP3 ภาษาไทย |

### โฟลเดอร์ vault

```
Baby_learning/
├── raw/        ข้อมูลดิบจากแต่ละ source ต่อ topic
├── wiki/       สรุป wiki ภาษาอังกฤษ พร้อม backlinks
├── scripts/    script ภาษาไทย สำหรับ TikTok/YouTube
├── tts/        ไฟล์เสียง MP3 จาก generate_tts.py
├── assets/     รูปภาพ local (Local Images Plus จัดการให้อัตโนมัติ)
└── logs/       log การรัน pipeline แต่ละวัน
```

---

## การทำงานของระบบ

### Pipeline flow (รันทุกวันตี 6 อัตโนมัติ)

```
Windows Task Scheduler ตี 6
  → run_pipeline.bat
      → Claude Code อ่าน CLAUDE.md
          → STEP 1: อ่าน config.yaml + inbox.md + scan wiki/
          → STEP 2: เลือก 3 topics (inbox ก่อน → auto-select ถ้าไม่พอ)
          → STEP 3: ต่อ topic: WebSearch → raw/ → wiki/ → scripts/
          → STEP 4: อัปเดต _index.md
          → STEP 5: เขียน log
      → generate_tts.py แปลง scripts ใหม่เป็น MP3 ใน tts/
```

### Sources ที่ใช้ (เรียงตาม priority)
1. WHO
2. AAP (American Academy of Pediatrics)
3. Mayo Clinic
4. NHS
5. PubMed / Google Scholar
6. Thai medical guidelines (กรมอนามัย, แพทยสภา, Siriraj)

---

## การตั้งค่า (แก้ได้ใน Obsidian)

### config.yaml — ตั้งค่าหลัก
```yaml
schedule:
  topics_per_day: 3      # เปลี่ยนเป็น 2 ถ้า Pro limit
content:
  script_formats:
    formats: [hook-content-cta, storytelling, qa-mythbusting]
```

### inbox.md — เพิ่ม topic ล่วงหน้า
```markdown
## Pending Topics
- วิธีรับมือ colic ในทารกแรกเกิด
- การอาบน้ำทารกแรกเกิดที่ถูกวิธี
```

---

## Persona ของผู้พูด (ใช้ในทุก script)

- **Role:** General Practitioner (MD)
- **Background:** Health Informatics, MBA
- **งานปัจจุบัน:** Data Analyst ที่บริษัท Telemedicine
- **Tone:** evidence-based, approachable, data-driven
- **ภาษา:** ไทย — ทับศัพท์อังกฤษได้ แต่ต้องมีวงเล็บอธิบายภาษาไทยตามหลัง
  - ตัวอย่าง: SIDS (กลุ่มอาการเสียชีวิตกะทันหันในทารก), Latch (การอมหัวนมที่ถูกวิธี)

---

## Script Formats (rotate อัตโนมัติ)

| Format | รูปแบบ |
|---|---|
| `hook-content-cta` | hook แรก 5 วิ → เนื้อหา 4 นาที → CTA 30 วิ |
| `storytelling` | "พ่อมือใหม่หลายคนไม่รู้ว่า..." → ความรู้ → takeaway |
| `qa-mythbusting` | myth/คำถาม → ตอบด้วยข้อมูลทางการแพทย์ → guidance |

---

## TTS (Text-to-Speech)

- **Library:** edge-tts (ฟรี, Microsoft Neural TTS)
- **Voice:** `th-TH-NiwatNeural` (ชาย)
- **เปลี่ยนเป็นเสียงหญิง:** แก้ใน `generate_tts.py` บรรทัด `VOICE = "th-TH-PremwadeeNeural"`
- **รันแยก:** `python generate_tts.py` ใน PowerShell
- **รันอัตโนมัติ:** รวมใน `run_pipeline.bat` แล้ว

---

## Obsidian Plugins ที่ติดตั้ง

| Plugin | หน้าที่ |
|---|---|
| Local Images Plus | download รูปจากเว็บมาเก็บใน `assets/` อัตโนมัติ |

---

## Windows Task Scheduler

- **Task name:** Baby Learning Pipeline
- **Schedule:** Daily 06:00
- **Wake from sleep:** เปิดแล้ว ✅
- **Action:** รัน `run_pipeline.bat`
- **สำคัญ:** ก่อนนอนให้ **Sleep** (ไม่ใช่ Shutdown)

---

## สิ่งที่ทำไปแล้ววันนี้ (2026-04-29)

Pipeline รันครั้งแรกสำเร็จ สร้างไฟล์:
- `wiki/newborn-safe-sleep.md` — Newborn Safe Sleep (SIDS prevention)
- `wiki/breastfeeding-basics.md` — Breastfeeding Basics
- `wiki/newborn-jaundice.md` — Newborn Jaundice (hyperbilirubinemia)
- `scripts/2026-04-29-newborn-safe-sleep.md` *(hook-content-cta)*
- `scripts/2026-04-29-breastfeeding-basics.md` *(storytelling)*
- `scripts/2026-04-29-newborn-jaundice.md` *(qa-mythbusting)*
- `tts/` — MP3 ทั้ง 3 ไฟล์

---

## Next Steps ที่อาจทำต่อ

- [ ] ทดสอบ wake-from-sleep จริงๆ ว่า Task Scheduler ปลุกเครื่องได้
- [ ] ดู script ที่สร้างแล้วว่าคุณภาพเป็นยังไง ปรับ CLAUDE.md ถ้าต้องการ
- [ ] พิจารณา ElevenLabs voice cloning ถ้าอยากได้เสียงตัวเอง
- [ ] เพิ่ม topic ใน inbox.md สำหรับวันพรุ่งนี้
- [ ] เพิ่ม Obsidian Web Clipper ใน Chrome เพื่อ clip บทความเพิ่มเติมด้วยตัวเอง

---

## วิธีรัน Manual (ถ้าอยากรันนอกเวลาตี 6)

```powershell
cd "C:\Users\wongt\Desktop\Baby_learning"
.\run_pipeline.bat
```

หรือรัน TTS อย่างเดียว:
```powershell
cd "C:\Users\wongt\Desktop\Baby_learning"
python generate_tts.py
```
