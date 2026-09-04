# pib-ml-data

Turns raw photos into two ready-to-train datasets: card-pose detection and
penis segmentation. Everything is scripted as a [DVC](https://dvc.org)
pipeline in `process_models/` — resize, verify labels, then filter into
the final datasets based on `metadata.csv`.

## Setup

```bash
uv sync
source .venv/bin/activate
```

Requires AWS credentials for the S3 remote (`s3://dvc-tales/pib-data`).

## Run the pipeline

```bash
cd process_models
dvc pull      # fetch raw data + labels from S3
dvc repro     # run every stage, only re-running what changed
```

Outputs land in `process_models/`:

- `card_pose_dataset/` — images + pose labels
- `penis_segmentation_dataset/` — images + masks
- `cleaned/` — images + labels + masks + metadata, final filtered dataset

Push new results back with `dvc push`.

See [AGENTS.md](AGENTS.md) for how the pipeline is structured internally.
