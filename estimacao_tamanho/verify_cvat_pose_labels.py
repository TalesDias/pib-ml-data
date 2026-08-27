"""Verify that card_pose_labels/ has a .txt label for every image in resized/."""

import sys
from pathlib import Path

RESIZED_DIR = Path("resized")
LABELS_DIR = Path("card_pose_labels")


def main() -> None:
    LABELS_DIR.mkdir(exist_ok=True)

    images = {f.stem for f in RESIZED_DIR.iterdir() if f.is_file()}
    labels = {f.stem for f in LABELS_DIR.iterdir() if f.is_file() and f.suffix == ".txt"}

    missing_labels = sorted(images - labels)
    extra_labels = sorted(labels - images)

    if not missing_labels and not extra_labels:
        print(f"OK. {len(images)} images and {len(labels)} labels match.")
        return

    print(f"Mismatch: {len(images)} images in '{RESIZED_DIR}/', {len(labels)} labels in '{LABELS_DIR}/'.")

    if missing_labels:
        print(f"{len(missing_labels)} missing label(s), showing first 5:")
        for stem in missing_labels[:5]:
            print(f"  {stem}.jpg")

    if extra_labels:
        print(f"{len(extra_labels)} extra label(s) with no matching image, showing first 5:")
        for stem in extra_labels[:5]:
            print(f"  {stem}.txt")

    sys.exit(1)

if __name__ == "__main__":
    main()
