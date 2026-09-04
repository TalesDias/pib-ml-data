"""Copy process_models/penis_segmentation_dataset into penis_segmentation/models/."""

import shutil
from pathlib import Path

SRC_DIR = Path("../process_models/penis_segmentation_dataset")
DST_DIR = Path("models")


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def main() -> None:
    reset_dir(DST_DIR / "images")
    reset_dir(DST_DIR / "masks")

    n = 0
    for src in sorted((SRC_DIR / "images").iterdir()):
        shutil.copy2(src, DST_DIR / "images" / src.name)
        n += 1
    for src in sorted((SRC_DIR / "masks").iterdir()):
        shutil.copy2(src, DST_DIR / "masks" / src.name)

    print(f"Copied {n} image/mask pair(s) to '{DST_DIR}/'")


if __name__ == "__main__":
    main()
