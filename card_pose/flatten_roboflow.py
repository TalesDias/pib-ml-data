"""Flatten raw_roboflow/ (and new_roboflow/, if present) train/valid/test splits into roboflow/{images,labels}/."""

import shutil
from pathlib import Path

SOURCE_DIR = Path("raw_roboflow")
SPLITS = ["train", "valid", "test"]
DST_DIR = Path("roboflow")


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def main() -> None:
    reset_dir(DST_DIR / "images")
    reset_dir(DST_DIR / "labels")

    n = 0
    if not SOURCE_DIR.exists():
        print(f"Raw dir '{SOURCE_DIR}/' was not found")
    else: 
        for split in SPLITS:
            if not (SOURCE_DIR / split).exists():
                continue
            for img in sorted((SOURCE_DIR / split / "images").iterdir()):
                shutil.copy2(img, DST_DIR / "images" / img.name)
                n += 1
            for lbl in sorted((SOURCE_DIR / split / "labels").iterdir()):
                shutil.copy2(lbl, DST_DIR / "labels" / lbl.name)

    print(f"Copied {n} image/label pair(s) into '{DST_DIR}/'")


if __name__ == "__main__":
    main()
