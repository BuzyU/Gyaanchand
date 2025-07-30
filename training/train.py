from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset, Dataset, concatenate_datasets
import pandas as pd
import os
import json

# Load base tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct", trust_remote_code=True)

# Falcon may not have a pad_token by default
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    "tiiuae/falcon-7b-instruct",
    trust_remote_code=True,
    pad_token_id=tokenizer.pad_token_id
)

# Load JSON training data
json_path = "training/training_data_grammar.json"
with open(json_path) as f:
    json_data = json.load(f)

json_dataset = Dataset.from_list([
    {"text": d["prompt"] + "\n" + d["completion"]}
    for d in json_data
])

# Load CSV datasets
csv_datasets_dir = "datasets/processed/"
csv_files = [f for f in os.listdir(csv_datasets_dir) if f.endswith(".csv")]

csv_datasets = []
for file in csv_files:
    df = pd.read_csv(os.path.join(csv_datasets_dir, file))
    if {"prompt", "completion"}.issubset(df.columns):
        hf_ds = Dataset.from_pandas(df[["prompt", "completion"]])
        formatted = hf_ds.map(lambda ex: {"text": ex["prompt"] + "\n" + ex["completion"]})
        csv_datasets.append(formatted)

# Combine all datasets
all_datasets = [json_dataset] + csv_datasets
full_dataset = concatenate_datasets(all_datasets)

# Tokenize the dataset
def tokenize_fn(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

tokenized_dataset = full_dataset.map(tokenize_fn, batched=True)

# LoRA config
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["query_key_value"],  # Make sure this matches your base model's architecture
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)

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
    evaluation_strategy="no",
    logging_first_step=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()

# Save the final model
model.sav
