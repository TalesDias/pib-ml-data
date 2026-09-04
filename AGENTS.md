# pib-ml-data

DVC pipelines that prepare image datasets for card-pose estimation and penis
segmentation models. Three pipelines, each its own working
directory and `dvc.yaml`, each run via `dvc repro`:

- `process_models/` — turns raw captures into labeled, filtered datasets.
- `card_pose/` — assembles card-pose training sources.
- `penis_segmentation/` — assembles segmentation training sources.

`card_pose/` and `penis_segmentation/` depend directly on `process_models/`
outputs (as cross-directory `deps:` in their `dvc.yaml`), so running
`dvc repro` from either one also reproduces any stale `process_models/`
stages automatically — no need to `cd` there separately.

## process_models/ (dvc.yaml, run top to bottom via `dvc repro`)

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

### Key files

- `metadata.csv` — one row per sample, keyed by `Id` (matches file stems
  everywhere). Columns of note: `Pose_training`, `Seg_training`,
  `Pipeline_suitable` (each `Include`/`Exclude`), plus measurement fields.
  Parse with `csv.DictReader`/`DictWriter` — `Notes` has embedded commas.

## card_pose/ (dvc.yaml)

Assembles two independent, split-agnostic image sources so a downstream
training repo can decide train/val/test and which source(s) to use — and
when to fine-tune against them — on its own:

1. `prepare_models.py`: copies `../process_models/card_pose_dataset/` →
   `models/{images,labels}`.
2. `flatten_roboflow.py`: merges `raw_roboflow/{train,valid,test}/` (a raw
   Roboflow export) into flat `roboflow/{images,labels}`, dropping the split
   boundaries, READMEs, and `data.yaml`.

`raw_roboflow/` (raw download) and `testing/` (showcase videos) are static
inputs, not generated — tracked individually with `dvc add`
(`raw_roboflow.dvc`, `testing.dvc`), not wired into `dvc.yaml`.

## penis_segmentation/ (dvc.yaml)

Similar objective as `card_pose/`, but with only one source

1. `prepare_models.py`: copies
   `../process_models/penis_segmentation_dataset/` → `models/{images,masks}`.

## Conventions

- Stdlib only (`pathlib`, `csv`, `shutil`); no argparse, logging, or pandas.
- Scripts clear (`rmtree`) an output dir before rebuilding it, so re-runs are
  idempotent.
- Every stage lists its own script as a `deps:` entry in `dvc.yaml`, so
  editing a script forces re-execution.
- Every generated directory is git-ignored (DVC-tracked instead) via a
  `.gitignore` per pipeline directory.
