"""Join resized images and verified labels into labeled/, split into images/, card_poses/, and penis_masks/ subdirectories."""

import shutil
from pathlib import Path

RESIZED_DIR = Path("resized")
CARD_POSES_DIR = Path("card_pose_labels_verified")
PENIS_MASKS_DIR = Path("penis_segmentation_masks_verified")
METADATA_FILE = Path("metadata.csv")

LABELED_DIR = Path("labeled")
IMAGES_OUT = LABELED_DIR / "images"
CARD_POSES_OUT = LABELED_DIR / "card_poses"
PENIS_MASKS_OUT = LABELED_DIR / "penis_masks"
METADATA_FILE_OUT = LABELED_DIR / "metadata.csv"


def copy_dir(src: Path, dst: Path) -> int:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return sum(1 for f in dst.iterdir() if f.is_file())


def main() -> None:
    LABELED_DIR.mkdir(exist_ok=True)

    shutil.copy(METADATA_FILE, METADATA_FILE_OUT)
    print(f"Copied metadata.csv to '{METADATA_FILE_OUT}'")

    n_images = copy_dir(RESIZED_DIR, IMAGES_OUT)
    print(f"Copied {n_images} image(s) to '{IMAGES_OUT}/'")

    n_card_poses = copy_dir(CARD_POSES_DIR, CARD_POSES_OUT)
    print(f"Copied {n_card_poses} card pose label(s) to '{CARD_POSES_OUT}/'")

    n_penis_masks = copy_dir(PENIS_MASKS_DIR, PENIS_MASKS_OUT)
    print(f"Copied {n_penis_masks} penis mask(s) to '{PENIS_MASKS_OUT}/'")


if __name__ == "__main__":
    main()
