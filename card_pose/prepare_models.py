"""Copy estimacao_tamanho/card_pose_dataset into card_pose/models/."""

import shutil
from pathlib import Path

SRC_DIR = Path("../estimacao_tamanho/card_pose_dataset")
DST_DIR = Path("models")


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def main() -> None:
    reset_dir(DST_DIR / "images")
    reset_dir(DST_DIR / "labels")

    n = 0
    for src in sorted((SRC_DIR / "images").iterdir()):
        shutil.copy2(src, DST_DIR / "images" / src.name)
        n += 1
    for src in sorted((SRC_DIR / "labels").iterdir()):
        shutil.copy2(src, DST_DIR / "labels" / src.name)

    print(f"Copied {n} image/label pair(s) to '{DST_DIR}/'")


if __name__ == "__main__":
    main()
