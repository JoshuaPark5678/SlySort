# SlySort: Waste Sorter

Clean rebuild of a vibe-coded high-school project.

## Status

| Model | Dataset | Metric | Result |
|---|---|---|---|
| Classifier (ResNet50 transfer learning) | TrashNet studio photos | Test accuracy, per-class P/R | TBA |
| Detector (YOLO) | TACO real-world photos | mAP50 | TBA |

## Tracking policy

Datasets and model weights are git-ignored (too big, regenerable).
Training configs, split seeds, and metrics files are committed
so results are reproducible even if the machine dies.
