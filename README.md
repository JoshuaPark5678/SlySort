# SlySort — Waste Sorter

Clean rebuild of a high-school project (originally GarbSort, vibe-coded).
Goal: an honest, well-documented waste classifier with numbers I can defend.

## Status

| Model | Dataset | Metric | Result |
|---|---|---|---|
| Classifier (ResNet50 transfer learning) | TrashNet studio photos | Test accuracy, per-class P/R | TBA — to be rerun |
| Detector (YOLO) | TACO real-world photos | mAP50 | TBA — to be rerun |

## Tracking policy

Datasets and model weights are git-ignored (too big, regenerable).
Training configs, split seeds, and metrics files are committed —
so results are reproducible even if the machine dies.
