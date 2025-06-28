from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset


# Load fine-tuned model and tokenizer
model_path = 'fine_tuned_gpt3'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Generate response with adjusted settings
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True)
    outputs = model.generate(
        **inputs,
        max_length=15,
        num_return_sequences=1,
        temperature=0.7,  # Adjust temperature for more varied responses
        no_repeat_ngram_size=2  # Prevent repetition of n-grams
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Interactive chat
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = generate_response(user_input)
    print(f"Bot: {response}")
