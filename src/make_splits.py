# Make splits in the dataset 

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]  # src/make_splits.py -> SlySort/
ann_path = ROOT / "data" / "upstream" / "data" / "annotations.json"
cfg_path = ROOT / "configs" / "data.yaml"
out_path = ROOT / "metrics" / "splits.json"

import json

with open(ann_path, "r") as file:
    annotations = json.load(file)

image_ids = []

for image in annotations["images"]:
    image_ids.append(image["id"])

import random
import yaml

with open(cfg_path, "r") as file:
    seed = yaml.safe_load(file)["seed"]

random.Random(42).shuffle(image_ids)

# print(image_ids)

train = []
val = []
test = []

split_ratio = 0.15 

num_of_val = int(len(image_ids) * split_ratio) # around 15%

val = image_ids[:num_of_val]
test = image_ids[num_of_val:num_of_val*2]
train = image_ids[num_of_val * 2:]

print(len(val), len(test), len(train))

output = {
  "seed": seed,
  "ratios": [1 - 2* split_ratio, split_ratio, split_ratio],
  "train": train,
  "val": val,
  "test": test
}


with open(out_path, "w") as file:
    json.dump(output, file, indent=4)
