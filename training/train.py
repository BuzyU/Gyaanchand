from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
import json
from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd
import os

# Load base model
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct", trust_remote_code=True)

# Load JSON training data
json_path = "training/training_data_grammar.json"
with open(json_path) as f:
    json_data = json.load(f)

json_dataset = Dataset.from_list([{"text": d["prompt"] + "\n" + d["completion"]} for d in json_data])

# Load CSV datasets and convert to HF format
csv_datasets_dir = "datasets/processed/"
csv_files = [f for f in os.listdir(csv_datasets_dir) if f.endswith(".csv")]

csv_dataframes = []
for file in csv_files:
    df = pd.read_csv(os.path.join(csv_datasets_dir, file))
    if "prompt" in df.columns and "completion" in df.columns:
        csv_dataframes.append(Dataset.from_pandas(df[["prompt", "completion"]]))

# Combine all datasets
merged = [json_dataset]
for csv_ds in csv_dataframes:
    csv_formatted = csv_ds.map(lambda ex: {"text": ex["prompt"] + "\n" + ex["completion"]})
    merged.append(csv_formatted)

full_dataset = Dataset.concatenate_datasets(merged)

# Apply LoRA config
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["query_key_value"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)

# Tokenize
def tokenize_fn(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

full_dataset = full_dataset.map(tokenize_fn, batched=True)

# Training arguments
args = TrainingArguments(
    output_dir="training/gyaanchand-lora",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=50,
    logging_dir="logs",
    logging_steps=10,
    save_steps=200,
    save_total_limit=3,
    learning_rate=2e-4,
    fp16=True,
    evaluation_strategy="no"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=full_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()
model.save_pretrained("training/gyaanchand-lora")
tokenizer.save_pretrained("training/gyaanchand-lora")
