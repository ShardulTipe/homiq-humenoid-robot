from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
from datasets import load_dataset, DatasetDict, Features, Value

# Load pre-trained model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Add special tokens
tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

# Load model and resize token embeddings
model = GPT2LMHeadModel.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))
model = model.to('cuda')  # Move model to GPU

# Load dataset and tokenize
features = Features({'text': Value('string')})
data = load_dataset('text', data_files={'train': "C:/Users/shard/OneDrive/Desktop/dialogs.txt"}, features=features)
print(data['train'][0])
tokenized_data = data.map(lambda x: tokenizer(x['text'], truncation=True, padding='max_length'), batched=True)

# Define the DataCollator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# Training arguments with optimizations
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=2,  # Further reduce batch size
    gradient_accumulation_steps=8,  # Further accumulate gradients
    fp16=True,  # Enable mixed precision training
    save_steps=10_000,
    save_total_limit=2,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_data['train']
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained('fine_tuned_gpt2')
tokenizer.save_pretrained('fine_tuned_gpt2')

# Interactive chat
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load fine-tuned model
model_path = 'fine_tuned_gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
model = model.to('cuda')  # Ensure the model is on GPU

# Generate response
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True).to('cuda')
    outputs = model.generate(**inputs, max_length=10, num_return_sequences=1, temperature=0.7, no_repeat_ngram_size=2)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Interactive chat
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = generate_response(user_input)
    print(f"Bot: {response}")
