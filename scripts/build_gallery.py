import json
import re
import sys
import urllib.parse
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "references"
DATA_FILE = ROOT / "_data" / "gallery.json"
IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
THUMB_DIR = "thumbs"
THUMB_SIZE = (960, 960)
SMALL_ENOUGH = 300 * 1024


def natural_key(name):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", name)]


def is_small(source):
    with Image.open(source) as image:
        width, height = image.size
    return (
        width <= THUMB_SIZE[0]
        and height <= THUMB_SIZE[1]
        and source.stat().st_size <= SMALL_ENOUGH
    )


def make_thumb(source, target):
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode not in ("RGB", "L"):
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.convert("RGBA").getchannel("A"))
            image = background
        image.thumbnail(THUMB_SIZE, Image.LANCZOS)
        target.parent.mkdir(exist_ok=True)
        image.save(target, "JPEG", quality=82, optimize=True, progressive=True)


def build_category(folder):
    images = sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_TYPES),
        key=lambda p: natural_key(p.name),
    )
    entries = []
    wanted = set()
    for source in images:
        src = urllib.parse.quote(source.name)
        thumb = folder / THUMB_DIR / (source.name + ".jpg")
        try:
            if is_small(source):
                entries.append({"src": src, "thumb": src})
                continue
            make_thumb(source, thumb)
        except OSError as error:
            print(f"Hoppar över {source.relative_to(ROOT)}: {error}", file=sys.stderr)
            continue
        wanted.add(thumb.name)
        entries.append({"src": src, "thumb": f"{THUMB_DIR}/{urllib.parse.quote(thumb.name)}"})

    thumbs = folder / THUMB_DIR
    if thumbs.is_dir():
        for old in thumbs.iterdir():
            if old.name not in wanted:
                old.unlink()
        if not any(thumbs.iterdir()):
            thumbs.rmdir()
    return entries


def main():
    gallery = {}
    for folder in sorted(p for p in REFERENCES.iterdir() if (p / "index.html").is_file()):
        gallery[folder.name] = build_category(folder)
        print(f"{folder.name}: {len(gallery[folder.name])} bilder")
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(gallery, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
