"""Build card_pose_dataset/, penis_segmentation_dataset/, and cleaned/ training datasets from labeled/, filtered by metadata.csv inclusion flags."""

import csv
import shutil
from pathlib import Path

LABELED_DIR = Path("labeled")

IMAGES_DIR = LABELED_DIR / "images"
CARD_POSES_DIR = LABELED_DIR / "card_poses"
PENIS_MASKS_DIR = LABELED_DIR / "penis_masks"
METADATA_FILE = Path("metadata.csv")

CARD_POSE_DATASET_DIR = Path("card_pose_dataset")
PENIS_SEGMENTATION_DATASET_DIR = Path("penis_segmentation_dataset")
CLEANED_DIR = Path("cleaned")


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def copy_included(rows, flag: str, src_dir: Path, dst_dir: Path) -> int:
    """Copy the file for every row where row[flag] == 'Include' from src_dir to dst_dir."""
    included = [row for row in rows if row[flag] == "Include"]
    for row in included:
        src = next(src_dir.glob(f"{row['Id']}.*"))
        shutil.copy2(src, dst_dir / src.name)
    return len(included)


def write_cleaned_metadata(rows, fieldnames) -> int:
    included = [row for row in rows if row["Pipeline_suitable"] == "Include"]
    with open(CLEANED_DIR / "metadata.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(included)
    return len(included)


def main() -> None:
    with open(METADATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    reset_dir(CARD_POSE_DATASET_DIR / "images")
    reset_dir(CARD_POSE_DATASET_DIR / "labels")
    n_pose = copy_included(rows, "Pose_training", IMAGES_DIR, CARD_POSE_DATASET_DIR / "images")
    copy_included(rows, "Pose_training", CARD_POSES_DIR, CARD_POSE_DATASET_DIR / "labels")
    print(f"Copied {n_pose} image/label pair(s) to '{CARD_POSE_DATASET_DIR}/'")

    reset_dir(PENIS_SEGMENTATION_DATASET_DIR / "images")
    reset_dir(PENIS_SEGMENTATION_DATASET_DIR / "masks")
    n_seg = copy_included(rows, "Seg_training", IMAGES_DIR, PENIS_SEGMENTATION_DATASET_DIR / "images")
    copy_included(rows, "Seg_training", PENIS_MASKS_DIR, PENIS_SEGMENTATION_DATASET_DIR / "masks")
    print(f"Copied {n_seg} image/mask pair(s) to '{PENIS_SEGMENTATION_DATASET_DIR}/'")

    reset_dir(CLEANED_DIR / "images")
    reset_dir(CLEANED_DIR / "labels")
    reset_dir(CLEANED_DIR / "masks")
    n_cleaned = copy_included(rows, "Pipeline_suitable", IMAGES_DIR, CLEANED_DIR / "images")
    copy_included(rows, "Pipeline_suitable", CARD_POSES_DIR, CLEANED_DIR / "labels")
    copy_included(rows, "Pipeline_suitable", PENIS_MASKS_DIR, CLEANED_DIR / "masks")
    n_cleaned_rows = write_cleaned_metadata(rows, fieldnames)
    print(f"Copied {n_cleaned} image/label/mask triple(s) to '{CLEANED_DIR}/', wrote {n_cleaned_rows} metadata row(s)")


if __name__ == "__main__":
    main()
