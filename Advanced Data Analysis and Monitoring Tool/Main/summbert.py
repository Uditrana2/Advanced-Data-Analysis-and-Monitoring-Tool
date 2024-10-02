from transformers import BertTokenizer, BertForConditionalGeneration

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
model = BertForConditionalGeneration.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Read the scraped text file
with open("scraped.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Tokenize the input text
inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

# Generate the summary
summary_ids = model.generate(inputs["input_ids"], max_length=150, num_beams=2, length_penalty=2.0, early_stopping=True)

# Decode the summary tokens back to text
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Output the summary
print("Summary:")
print(summary)
