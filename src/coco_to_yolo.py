# Convert Coco label format to Yolo label format
# Coco:  [x_topLeft, y_topLeft, width, height]
# Yolo:  class_id x_center y_center width height

from pathlib import Path
import json
import csv

ROOT = Path(__file__).resolve().parents[1]
splits = json.load(open(ROOT / "metrics" / "splits.json", encoding="utf-8"))
annotations = json.load(open(ROOT / "data" / "upstream" / "data" / "annotations.json", encoding="utf-8"))

# use map_10.csv for the classification
name_to_super = {}
with open(ROOT / "data" / "upstream" / "detector" / "taco_config" / "map_10.csv", encoding="utf-8") as f:
    for row in csv.reader(f):
        name_to_super[row[0]] = row[1]

# print(len(name_to_super))
# print(name_to_super)

# id
classes = sorted(set(name_to_super.values()))
class_to_id = {}
for i, name in enumerate(classes):
    class_to_id[name] = i

# image dimensions
img_dims = {}
for img in annotations["images"]:
    img_dims[img["id"]] = (img["width"], img["height"])

# iid to boxes dict
boxes_by_image = {}
for ann in annotations["annotations"]:
    iid = ann["image_id"]
    if iid not in boxes_by_image:
        boxes_by_image[iid] = []
    boxes_by_image[iid].append(ann)

print(classes)
print(len(boxes_by_image))

id_to_name = {}
for c in annotations["categories"]:
    id_to_name[c["id"]] = c["name"]

for split in ("train", "val", "test"):
    label_dir = ROOT / "data" / "yolo" / "labels" / split
    label_dir.mkdir(parents=True, exist_ok=True)
    for iid in splits[split]:
        img_w, img_h = img_dims[iid]
        lines = []
        for ann in boxes_by_image.get(iid, []):
            original = id_to_name[ann["category_id"]]
            if original not in name_to_super:
                raise KeyError("unmapped category: " + original)
            cid = class_to_id[name_to_super[original]]
            x, y, w, h = ann["bbox"]
            xc = (x + w / 2) / img_w
            yc = (y + h / 2) / img_h
            lines.append(str(cid) + " " + str(xc) + " " + str(yc) + " " + str(w / img_w) + " " + str(h / img_h))
        with open(label_dir / (str(iid) + ".txt"), "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")

with open(ROOT / "metrics" / "classes.json", "w", encoding="utf-8") as f:
    json.dump(classes, f, indent=2)

print("wrote labels")
