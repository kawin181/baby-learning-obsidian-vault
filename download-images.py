"""
Baby Learning — Image Downloader (Pixabay API)
License: Pixabay License = free for commercial & non-commercial use, no attribution required.
Docs: https://pixabay.com/api/docs/
"""
import re
import time
import requests
from pathlib import Path

API_KEY = "55660748-80685919568cc0370dbdc214a"
BASE = Path("short-clip")
DELAY = 1.5        # seconds between downloads
IMAGES_PER_TOPIC = 8

# Search queries per topic (tries each query in order until 8 images collected)
TOPICS = {
    "newborn-jaundice": [
        "newborn jaundice yellow baby",
        "phototherapy baby blue light",
        "jaundice infant hospital",
        "newborn baby doctor checkup",
    ],
    "newborn-safe-sleep": [
        "baby sleeping crib safe",
        "newborn sleeping back",
        "baby bassinet bedroom",
        "infant safe sleep",
    ],
    "baby-gas-burping": [
        "father burping baby",
        "burping newborn shoulder",
        "baby crying stomach pain",
        "bottle feeding newborn",
        "baby massage tummy",
    ],
    "newborn-immunizations": [
        "baby vaccination injection",
        "infant vaccine pediatrician",
        "newborn hospital checkup",
        "baby doctor nurse",
    ],
    "newborn-weight-gain": [
        "baby weighing scale hospital",
        "newborn baby checkup pediatrician",
        "infant healthy growing baby",
        "newborn baby happy healthy",
        "baby monthly growth",
    ],
    "formula-feeding-basics": [
        "baby bottle milk newborn",
        "infant drinking bottle milk",
        "father feeding newborn bottle",
        "baby milk feeding close up",
    ],
    "baby-crying-soothing": [
        "soothing crying baby",
        "swaddled newborn baby",
        "father holding newborn skin contact",
        "crying infant newborn",
        "parent comfort newborn",
    ],
}


def search_pixabay(query: str, n: int = 10) -> list[dict]:
    url = "https://pixabay.com/api/"
    params = {
        "key": API_KEY,
        "q": query,
        "image_type": "photo",
        "safesearch": "true",
        "per_page": n,
        "lang": "en",
        "order": "popular",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("hits", [])


def slug(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:30]


def download_image(url: str, out_path: Path) -> bool:
    r = requests.get(url, timeout=30)
    if r.status_code != 200 or len(r.content) < 5000:
        return False
    out_path.write_bytes(r.content)
    return True


def build_attribution_block(downloaded: list[dict]) -> str:
    lines = [
        "",
        "## Attribution",
        "",
        "| File | Author | License | Pixabay URL |",
        "|------|--------|---------|-------------|",
    ]
    for item in downloaded:
        fname = item["filename"]
        user = item["user"]
        pid = item["id"]
        page = f"https://pixabay.com/photos/{pid}/"
        lines.append(f"| {fname} | {user} | Pixabay License (free) | {page} |")
    lines.append("")
    lines.append("> Pixabay License: free for commercial & non-commercial use, no attribution required.")
    return "\n".join(lines)


def update_tts_script(folder: Path, downloaded: list[dict]):
    script = folder / "tts-script.md"
    if not script.exists():
        return
    content = script.read_text(encoding="utf-8")

    # Replace everything from "## Attribution" to end-of-file
    new_attr = build_attribution_block(downloaded)
    if "## Attribution" in content:
        content = re.sub(r"\n## Attribution.*", new_attr, content, flags=re.DOTALL)
    else:
        content = content.rstrip() + "\n" + new_attr

    script.write_text(content, encoding="utf-8")


def process_topic(topic: str, queries: list[str]):
    folder = BASE / topic
    folder.mkdir(parents=True, exist_ok=True)

    # Skip if already has enough images
    existing = [f for f in folder.iterdir()
                if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    if len(existing) >= IMAGES_PER_TOPIC:
        print(f"  SKIP — already has {len(existing)} images")
        return

    collected: list[dict] = []
    seen_ids: set[int] = set()

    for query in queries:
        if len(collected) >= IMAGES_PER_TOPIC:
            break
        hits = search_pixabay(query, n=10)
        for hit in hits:
            if len(collected) >= IMAGES_PER_TOPIC:
                break
            if hit["id"] in seen_ids:
                continue
            seen_ids.add(hit["id"])

            idx = len(collected) + 1
            ext = hit["largeImageURL"].split("?")[0].rsplit(".", 1)[-1].lower()
            tag_slug = slug(hit["tags"].split(",")[0])
            fname = f"{idx:02d}-{tag_slug}.{ext}"
            out = folder / fname

            if download_image(hit["largeImageURL"], out):
                size_kb = out.stat().st_size // 1024
                print(f"  [{idx:02d}] {fname} ({size_kb} KB) — by {hit['user']}")
                collected.append({"filename": fname, "user": hit["user"], "id": hit["id"]})
                time.sleep(DELAY)
            else:
                print(f"  FAIL {fname}")

    if collected:
        update_tts_script(folder, collected)
        print(f"  Attribution updated in tts-script.md")


def main():
    print("=" * 55)
    print("  Baby Learning — Pixabay Image Downloader")
    print("=" * 55)
    for topic, queries in TOPICS.items():
        print(f"\n[{topic}]")
        process_topic(topic, queries)
    print("\nDone.")


if __name__ == "__main__":
    main()
