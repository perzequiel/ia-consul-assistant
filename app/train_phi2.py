from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
import torch

MODEL_NAME = "microsoft/phi-2"  # usarás phi-3-mini cuando esté en Hugging Face
dataset = load_dataset("json", data_files="finetune_phi_data.jsonl")["train"]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

def tokenize(example):
    prompt = f"Paciente: {example['input']}\nConsultorio:"
    full = prompt + " " + example["output"]
    return tokenizer(full, truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, load_in_8bit=True, device_map="auto")
peft_config = LoraConfig(task_type=TaskType.CAUSAL_LM, inference_mode=False, r=8, lora_alpha=32, lora_dropout=0.05)
model = get_peft_model(model, peft_config)

training_args = TrainingArguments(
    output_dir="phi-medico-model",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    logging_steps=10,
    save_total_limit=1,
    fp16=True,
)

trainer = Trainer(
    model=model,
    train_dataset=tokenized_dataset,
    args=training_args,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()
model.save_pretrained("phi-medico-model")
tokenizer.save_pretrained("phi-medico-model")
