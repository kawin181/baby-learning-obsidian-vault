import asyncio
import edge_tts
import os
import re
from pathlib import Path

VOICE = "th-TH-NiwatNeural"
SCRIPTS_DIR = Path("scripts")
TTS_DIR = Path("tts")


def extract_speech_text(md_content: str) -> str:
    # Remove front matter
    content = re.sub(r"^---.*?---\s*", "", md_content, flags=re.DOTALL)

    # Remove Speaker Notes section and everything after it
    content = re.sub(r"## Speaker Notes.*", "", content, flags=re.DOTALL)

    # Remove markdown heading markers but keep text on same line
    content = re.sub(r"^#{1,6}\s*", "", content, flags=re.MULTILINE)

    # Remove emoji + time markers like (0–5 วินาที), (~4 นาที)
    content = re.sub(r"🎬|📖|📢", "", content)
    content = re.sub(r"\(~?[\d–-]+\s*วินาที\)", "", content)
    content = re.sub(r"\(~?[\d–-]+\s*นาที\)", "", content)

    # Clean up
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


async def generate_audio(text: str, output_path: Path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(output_path))


async def main():
    TTS_DIR.mkdir(exist_ok=True)

    script_files = sorted(SCRIPTS_DIR.glob("*.md"))
    if not script_files:
        print("No script files found in scripts/")
        return

    for script_file in script_files:
        audio_file = TTS_DIR / (script_file.stem + ".mp3")

        if audio_file.exists():
            print(f"Skip  {script_file.name} (audio already exists)")
            continue

        content = script_file.read_text(encoding="utf-8")
        speech_text = extract_speech_text(content)

        if not speech_text.strip():
            print(f"Warn  {script_file.name} — no speakable text found")
            continue

        print(f"Gen   {script_file.name} -> {audio_file.name}")
        await generate_audio(speech_text, audio_file)
        print(f"Done  {audio_file.name}")


if __name__ == "__main__":
    asyncio.run(main())
