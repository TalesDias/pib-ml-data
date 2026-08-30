"""Verify that penis_segmentation_masks/ has a verification .json for every image in resized/, then copy the .png masks into penis_segmentation_masks_verified/.

Not every image has a corresponding .png mask (e.g. no penis visible in frame) - that's expected and isn't an error. The .json is what marks an image as verified."""

import shutil
import sys
from pathlib import Path

RESIZED_DIR = Path("resized")
LABELS_DIR = Path("penis_segmentation_masks")
VERIFIED_DIR = Path("penis_segmentation_masks_verified")


def main() -> None:
    LABELS_DIR.mkdir(exist_ok=True)

    images = {f.stem for f in RESIZED_DIR.iterdir() if f.is_file()}
    verified = {
        f.name[: -len("_pts.json")]
        for f in LABELS_DIR.iterdir()
        if f.is_file() and f.name.endswith("_pts.json")
    }

    missing_verifications = sorted(images - verified)
    extra_verifications = sorted(verified - images)

    if missing_verifications or extra_verifications:
        print(f"Mismatch: {len(images)} images in '{RESIZED_DIR}/', {len(verified)} verifications in '{LABELS_DIR}/'.")

        if missing_verifications:
            print(f"{len(missing_verifications)} missing verification(s), showing first 5:")
            for stem in missing_verifications[:5]:
                print(f"  {stem}_pts.json")

        if extra_verifications:
            print(f"{len(extra_verifications)} extra verification(s) with no matching image, showing first 5:")
            for stem in extra_verifications[:5]:
                print(f"  {stem}_pts.json")

        sys.exit(1)

    labels = {f.stem for f in LABELS_DIR.iterdir() if f.is_file() and f.suffix == ".png"}
    print(f"OK. {len(images)} images all verified, {len(labels)} have a mask.")

    if VERIFIED_DIR.exists():
        shutil.rmtree(VERIFIED_DIR)
    VERIFIED_DIR.mkdir()
    for stem in labels:
        shutil.copy2(LABELS_DIR / f"{stem}.png", VERIFIED_DIR / f"{stem}.png")
    print(f"Copied {len(labels)} verified mask(s) to '{VERIFIED_DIR}/'")


if __name__ == "__main__":
    main()
