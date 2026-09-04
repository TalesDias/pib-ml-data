# pib-ml-data

DVC pipeline that prepares image datasets for card-pose estimation and penis
segmentation models. The pipeline lives in `process_models/` and every
stage runs with that directory as the working directory.

## Pipeline (dvc.yaml, run top to bottom via `dvc repro`)

1. `flatten.py`: `raw/` → `flattened/` (flatten nested capture folders).
2. `resize.py`: `flattened/` → `resized/`.
3. `verify_cvat_pose_labels.py`: checks `card_pose_labels/` (CVAT) has a
   `.txt` per image in `resized/` → `card_pose_labels_verified/`.
4. `verify_sam_mask_labels.py`: checks `penis_segmentation_masks/` (SAM) has
   a verification `.json` per image → `penis_segmentation_masks_verified/`
   (`.png` masks only, not every image has one).
5. `join_labels.py`: merges `resized/` + both `_verified/` dirs into
   `labeled/{images,card_poses,penis_masks}/`.
6. `build_datasets.py`: reads `metadata.csv` and filters `labeled/` into:
   - `card_pose_dataset/{images,labels}/` — rows with `Pose_training=Include`
   - `penis_segmentation_dataset/{images,masks}/` — rows with `Seg_training=Include`
   - `cleaned/{images,labels,masks}/` + `cleaned/metadata.csv` — rows with
     `Pipeline_suitable=Include` (final, model-ready dataset)

## Key files

- `metadata.csv` — one row per sample, keyed by `Id` (matches file stems
  everywhere). Columns of note: `Pose_training`, `Seg_training`,
  `Pipeline_suitable` (each `Include`/`Exclude`), plus measurement fields.
  Parse with `csv.DictReader`/`DictWriter` — `Notes` has embedded commas.
- `dvc.yaml` / `dvc.lock` — stage definitions and pinned hashes.
- `.gitignore` — every generated directory is DVC-tracked, not git-tracked.

## Conventions

- Stdlib only (`pathlib`, `csv`, `shutil`); no argparse, logging, or pandas.
- Scripts clear (`rmtree`) an output dir before rebuilding it, so re-runs are
  idempotent.
- Every stage lists its own script as a `deps:` entry in `dvc.yaml`, so
  editing a script forces re-execution.
