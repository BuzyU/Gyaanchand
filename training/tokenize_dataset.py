from transformers import AutoTokenizer
import json

tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")

with open("datasets/processed/combined.json", "r", encoding="utf-8") as f:
    data = json.load(f)

tokenized_data = []
for sample in data:
    prompt = sample["instruction"]
    output = sample["output"]
    text = f"### Instruction:\n{prompt}\n\n### Response:\n{output}"
    tokenized_data.append(tokenizer(text, truncation=True, max_length=512))

print("Tokenization complete.")
