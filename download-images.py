"""
Download pending images for short-clip folders.
Run this script when Wikimedia rate limit resets (wait ~10 min after last attempt).
"""
import time
import requests
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
BASE = Path("short-clip")
DELAY = 4  # seconds between downloads

IMAGES = {
    "newborn-jaundice": [
        ("03-jaundice-diagram.png",    "https://upload.wikimedia.org/wikipedia/commons/b/b0/Jaundice.png"),
        ("04-neonatal-chart.png",      "https://upload.wikimedia.org/wikipedia/commons/8/85/Neonatal_jaundice.png"),
        ("05-phototherapy-baby.jpg",   "https://upload.wikimedia.org/wikipedia/commons/d/d9/Jaundice_phototherapy.jpg"),
        ("06-phototherapy-airforce.jpg","https://upload.wikimedia.org/wikipedia/commons/8/8c/Baby_receives_phototherapy_during_Operation_Allies_Refuge_%286820837%29.jpg"),
        ("07-phototherapy-cabinet.jpg","https://upload.wikimedia.org/wikipedia/commons/0/04/Cabine_de_phototh%C3%A9rapie_ferm%C3%A9e.jpg"),
    ],
    "newborn-safe-sleep": [
        ("01-baby-sleeping-back.jpg",     "https://upload.wikimedia.org/wikipedia/commons/2/25/Sleeping-baby_%28cropped%29.jpg"),
        ("02-safe-sleep-firm-surface.jpg","https://upload.wikimedia.org/wikipedia/commons/7/71/Safe_Infant_Sleep_Tip_Firm_Flat_Surface_%2844707786394%29.jpg"),
        ("03-safe-sleep-no-toys.jpg",     "https://upload.wikimedia.org/wikipedia/commons/9/98/Safe_to_Sleep_Tip_No_Toys_%2844707786624%29.jpg"),
        ("04-sids-awareness.jpg",         "https://upload.wikimedia.org/wikipedia/commons/2/2e/Safe_Infant_Sleep_for_SIDS_Awareness_Month_%2848842727393%29.jpg"),
        ("05-safe-sleep-back.jpg",        "https://upload.wikimedia.org/wikipedia/commons/e/e8/Safe_to_Sleep_Tip_Place_Baby_on_Back_%2844707780804%29.jpg"),
    ],
    # Topics below need image search first — run pipeline step 3e manually or search Wikimedia
    # "baby-gas-burping": [],
    # "newborn-immunizations": [],
    # "newborn-weight-gain": [],
    # "formula-feeding-basics": [],
    # "baby-crying-soothing": [],
}


def download(folder, filename, url):
    out = BASE / folder / filename
    if out.exists() and out.stat().st_size > 5000:
        print(f"  SKIP {filename} (already exists)")
        return True

    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    if r.status_code == 429:
        print(f"  RATE LIMIT — wait and retry later")
        return False
    if r.status_code != 200 or len(r.content) < 5000:
        print(f"  FAIL {filename} (status {r.status_code}, {len(r.content)} bytes)")
        return False

    out.write_bytes(r.content)
    print(f"  OK   {filename} ({len(r.content)//1024} KB)")
    return True


def main():
    print("Baby Learning — Image Downloader")
    print(f"Delay between downloads: {DELAY}s\n")

    for folder, images in IMAGES.items():
        print(f"[{folder}]")
        (BASE / folder).mkdir(parents=True, exist_ok=True)
        for filename, url in images:
            success = download(folder, filename, url)
            if not success and "RATE LIMIT" in str(success):
                print("Stopping — rate limited. Wait 10 min and retry.")
                return
            time.sleep(DELAY)
        print()

    print("Done.")


if __name__ == "__main__":
    main()
