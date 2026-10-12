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

random.Random(seed).shuffle(image_ids)

# print(image_ids)

train = []
val = []
test = []

split_ratio = 0.15 

num_of_val = int(len(image_ids) * split_ratio) # around 15%

val = image_ids[:num_of_val]
test = image_ids[num_of_val:num_of_val*2]
train = image_ids[num_of_val * 2:]

image_to_split = {}
for iid in train:
    image_to_split[iid] = "train"

for iid in val:
    image_to_split[iid] = "val"

for iid in test:
    image_to_split[iid] = "test"


# annotations into split
split_counts = {"train": {}, "val": {}, "test": {}}

for ann in annotations["annotations"]:
    split = image_to_split[ann["image_id"]]
    cid = ann["category_id"]
    split_counts[split][cid] = split_counts[split].get(cid, 0) + 1
   
# make category keys into readable keys

# ID to Name
id_to_name = {}
for c in annotations["categories"]:
    id_to_name[c["id"]] = c["name"]

# print top 5

def get_count(pair):
    return pair[1]

for split in ("train", "val", "test"):
    counts = split_counts[split]
    items = list(counts.items())
    items.sort(key=get_count, reverse=True)
    top5 = items[:5]
    print(split)
    for cid, n in top5:
        print(" ", id_to_name[cid], n)

# record the split with names instead of ids
named_counts = {}
for split in ("train", "val", "test"):
    named = {}
    for cid, n in split_counts[split].items():
        named[id_to_name[cid]] = n
    named_counts[split] = named

with open(ROOT / "metrics" / "split_class_counts.json", "w", encoding="utf-8") as f:
    json.dump(named_counts, f, indent=2)

output = {
  "seed": seed,
  "ratios": [1 - 2* split_ratio, split_ratio, split_ratio],
  "train": train,
  "val": val,
  "test": test
}


with open(out_path, "w") as file:
    json.dump(output, file, indent=4)

