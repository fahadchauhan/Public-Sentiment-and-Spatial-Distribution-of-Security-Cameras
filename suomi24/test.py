import torch
import pandas as pd
from transformers import MarianMTModel, MarianTokenizer

# Define the device to use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-fi-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name).to(device)

# Define the translation function
def translate(texts, tokenizer, model, device):
    # Process texts as a batch
    with torch.no_grad():
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        outputs = model.generate(**inputs)
        translated_texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return translated_texts

# Read CSV in chunks
chunk_size = 100  # Adjust the chunk size according to your GPU memory
separator = '<>'
filename = 'suomi24/Data/filtered/s24_2001.csv'
translated_filename = 'translated_output_file.csv'

# Create a CSV writer object to write rows to translated_filename
translated_file = open(translated_filename, 'w', newline='', encoding='utf-8')
csv_writer = pd.csv.writer(translated_file)

# Process the CSV in chunks
for chunk in pd.read_csv(filename, chunksize=chunk_size):
    # Combine columns with the chosen separator
    combined_texts = chunk.apply(lambda row: separator.join([str(row['title']), str(row['topic_name_top']), str(row['topic_name_leaf']), str(row['thread_text'])]), axis=1).tolist()
    
    # Translate texts
    translated_texts = translate(combined_texts, tokenizer, model, device)
    
    # Split the translated texts back into separate columns and write to file
    for text in translated_texts:
        parts = text.split(separator)
        if len(parts) != 4:  # Handle potential splitting errors
            parts = ['Translation Error'] * 4
        csv_writer.writerow(parts)

    print(f"Processed a chunk of size {chunk_size}")

# Close the translated file
translated_file.close()

print("Translation complete! The translated CSV is saved as 'translated_output_file.csv'.")
