# pib-ml-data

Turns raw photos into ready-to-train datasets for card-pose detection and
penis segmentation, as three independent [DVC](https://dvc.org) pipelines:

- `process_models/` — raw photos → resized, label-verified, filtered
  datasets, based on `metadata.csv`.
- `card_pose/` — assembles card-pose training sources: `models/` (from
  `process_models/`) plus `roboflow/` (a flattened Roboflow export). Leaves
  train/val/test splitting up to whichever repo trains on this data.
- `penis_segmentation/` — assembles segmentation training sources:
  `models/` (from `process_models/`).

## Setup

```bash
uv sync
source .venv/bin/activate
```

Requires AWS credentials for the S3 remote (`s3://dvc-tales/pib-data`).

## Run a pipeline

```bash
cd process_models   # or card_pose/, or penis_segmentation/
dvc pull      # fetch raw data + labels from S3
dvc repro     # run every stage, only re-running what changed
```

`card_pose/` and `penis_segmentation/` depend on `process_models/` outputs
directly, so `dvc repro` from either one also reproduces any stale
`process_models/` stages automatically.

## Outputs

- `process_models/card_pose_dataset/` — images + pose labels
- `process_models/penis_segmentation_dataset/` — images + masks
- `process_models/cleaned/` — images + labels + masks + metadata, final filtered dataset
- `card_pose/models/` — pose-labeled images sourced from `process_models/`
- `card_pose/roboflow/` — flattened Roboflow export (images + labels)
- `penis_segmentation/models/` — segmentation images + masks sourced from `process_models/`

Push new results back with `dvc push`.

See [AGENTS.md](AGENTS.md) for how each pipeline is structured internally.
