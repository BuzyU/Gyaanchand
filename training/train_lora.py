from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import torch

# Load dataset
dataset = load_dataset("json", data_files="datasets/processed/combined.json")

# Load tokenizer and model
model_id = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map="auto")

# PEFT config
peft_config = LoraConfig(
    r=8, lora_alpha=32, target_modules=["query_key_value"],
    lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

# Tokenization function
def tokenize(sample):
    text = f"### Instruction:\n{sample['instruction']}\n\n### Response:\n{sample['output']}"
    return tokenizer(text, truncation=True, padding="max_length", max_length=512)

tokenized = dataset["train"].map(tokenize, batched=False)

# Training args
args = TrainingArguments(
    output_dir="training/gyaanchand-lora",
    per_device_train_batch_size=2,
    num_train_epochs=2,
    logging_steps=10,
    save_steps=100,
    save_total_limit=2,
    fp16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()
