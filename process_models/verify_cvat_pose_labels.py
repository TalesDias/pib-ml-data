"""Verify that card_pose_labels/ has a .txt label for every image in resized/, then copy the labels into card_pose_labels_verified/."""

import shutil
import sys
from pathlib import Path

RESIZED_DIR = Path("resized")
LABELS_DIR = Path("card_pose_labels")
VERIFIED_DIR = Path("card_pose_labels_verified")


def main() -> None:
    LABELS_DIR.mkdir(exist_ok=True)

    images = {f.stem for f in RESIZED_DIR.iterdir() if f.is_file()}
    labels = {f.stem for f in LABELS_DIR.iterdir() if f.is_file() and f.suffix == ".txt"}

    missing_labels = sorted(images - labels)
    extra_labels = sorted(labels - images)

    if missing_labels or extra_labels:
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

    print(f"OK. {len(images)} images and {len(labels)} labels match.")

    if VERIFIED_DIR.exists():
        shutil.rmtree(VERIFIED_DIR)
    shutil.copytree(LABELS_DIR, VERIFIED_DIR)
    print(f"Copied verified labels to '{VERIFIED_DIR}/'")


if __name__ == "__main__":
    main()
