"""Resize flattened/ images so the largest dimension is MAX_SIZE, preserving aspect ratio, into resized/."""

import shutil
from pathlib import Path

from PIL import Image
from tqdm import tqdm

FLATTENED_DIR = Path("flattened")
RESIZED_DIR = Path("resized")
MAX_SIZE = 1280


def resize_image(src: Path, dst: Path) -> bool:
    """Resize src into dst if its largest dimension exceeds MAX_SIZE, else copy unchanged.

    Returns True if the image was resized, False if it was just copied.
    """
    with Image.open(src) as img:
        width, height = img.size
        if max(width, height) <= MAX_SIZE:
            shutil.copy2(src, dst)
            return False

        if width >= height:
            new_size = (MAX_SIZE, round(height * MAX_SIZE / width))
        else:
            new_size = (round(width * MAX_SIZE / height), MAX_SIZE)

        resized = img.resize(new_size, Image.LANCZOS)
        resized.save(dst)
        return True


def main() -> None:
    RESIZED_DIR.mkdir(exist_ok=True)

    files = sorted(f for f in FLATTENED_DIR.iterdir() if f.is_file())
    print(f"Resizing {len(files)} files from '{FLATTENED_DIR}/' (max dimension {MAX_SIZE}px)")

    resized_count = 0
    for f in tqdm(files, desc="resize"):
        if resize_image(f, RESIZED_DIR / f.name):
            resized_count += 1

    print(f"Done. {resized_count}/{len(files)} images resized, {len(files) - resized_count} copied unchanged.")
    print(f"Output saved to '{RESIZED_DIR}/'")


if __name__ == "__main__":
    main()
