"""Flatten raw/V0 and raw/V1 datasets into a single flatten/ folder with normalized names."""

import re
from pathlib import Path

from PIL import Image, ImageOps
from tqdm import tqdm

RAW_DIR = Path("raw")
FLATTENED_DIR = Path("flattened")

V1_NAME_RE = re.compile(r"(M\d+).*?(foto[12])", re.IGNORECASE)


def save_as_jpg(src: Path, dst: Path) -> None:
    """Save src as dst, applying any EXIF orientation to the pixels and dropping EXIF.

    A plain byte copy would keep the EXIF orientation tag, which later steps
    (e.g. resize) don't all respect the same way, leading to inconsistently
    rotated output down the pipeline.
    """
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img)
        img.convert("RGB").save(dst, "JPEG")


def flatten_v0(src_dir: Path) -> None:
    files = sorted(f for f in src_dir.iterdir() if f.is_file())
    print(f"V0: flattening {len(files)} files from '{src_dir.name}'")
    for f in tqdm(files, desc="V0"):
        save_as_jpg(f, FLATTENED_DIR / f"V0_{f.stem}.jpg")


def flatten_v1(src_dir: Path) -> None:
    files = sorted(f for f in src_dir.iterdir() if f.is_file())
    print(f"V1: flattening {len(files)} files from '{src_dir.name}'")
    for f in tqdm(files, desc="V1"):
        match = V1_NAME_RE.search(f.stem)
        if not match:
            print(f"V1: skipping unrecognized file name '{f.name}'")
            continue
        code, foto = match.group(1).upper(), match.group(2).lower()
        suffix = "_f1" if foto == "foto1" else "_f2"
        save_as_jpg(f, FLATTENED_DIR / f"V1_{code}{suffix}.jpg")


def main() -> None:
    FLATTENED_DIR.mkdir(exist_ok=True)

    v0_dir = next(p for p in RAW_DIR.glob("V0*") if p.is_dir())
    v1_dir = next(p for p in RAW_DIR.glob("V1*") if p.is_dir())

    flatten_v0(v0_dir)
    flatten_v1(v1_dir)

    print(f"Done. Flattened files saved to '{FLATTENED_DIR}/'")


if __name__ == "__main__":
    main()
