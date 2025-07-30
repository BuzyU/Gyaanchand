# preprocess.py
import os
import json

raw_path = "datasets/raw"
processed_path = "datasets/processed"
combined_data = []

for file in os.listdir(raw_path):
    if file.endswith(".json") or file.endswith(".jsonl"):
        with open(os.path.join(raw_path, file), "r", encoding="utf-8") as f:
            data = json.load(f)
            combined_data.extend(data)

# Create processed folder if it doesn't exist
os.makedirs(processed_path, exist_ok=True)

# Save combined data
with open(os.path.join(processed_path, "combined.json"), "w", encoding="utf-8") as f:
    json.dump(combined_data, f, indent=2)
