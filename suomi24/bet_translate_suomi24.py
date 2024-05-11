import torch
import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm

# Setup device for torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-fi-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name).to(device)

# Translation function
def translate(text, tokenizer, model, device):
    text = str(text)  # Ensure the input is always a string
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        outputs = model.generate(**inputs)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

# Function to write DataFrame chunk to CSV
def write_chunk_to_csv(df_chunk, file_path, mode='a', header="False"):
    
    df_chunk.to_csv(file_path, mode=mode, header=header, index=False)

# Read the CSV file into a DataFrame

input_file = 'C:/Users/user/Documents/suomi24/Data/filtered/s24_2005.csv'
output_file = "C:/Users/user/Documents/suomi24/Data/translated/s24_2005.csv"
chunk_size = 5000
df = pd.read_csv(input_file)
print(input_file)
# Initialize dictionaries to store translations
translated_titles = {}
translated_topic_names_top = {}
translated_topic_names_leaf = {}

# Initialize a list to accumulate processed rows
processed_rows = []
first_write = True
bet_check = False
# Process each row, translating as needed
for index, row in tqdm(df.iterrows()):
    thread_id = row['thread_id']
    
    if thread_id == 1464141:
        bet_check = True
    if not bet_check:
        continue
    # Check and translate the unique fields
    if thread_id not in translated_titles:

        # Every 50,000 rows, write to CSV and clear the list
        if len(processed_rows) > chunk_size:
            # if first_write:
            #     write_header = True
            #     write_mode = 'w'
            #     first_write=False
            # else:
            write_header = False
            write_mode = 'a'
            write_chunk_to_csv(pd.DataFrame(processed_rows), output_file, mode=write_mode, header=write_header)
            processed_rows = []

        translated_titles[thread_id] = translate(row['title'], tokenizer, model, device)
        translated_topic_names_top[thread_id] = translate(row['topic_name_top'], tokenizer, model, device)
        translated_topic_names_leaf[thread_id] = translate(row['topic_name_leaf'], tokenizer, model, device)
    
    # Assign the translations for unique fields
    row['title'] = translated_titles[thread_id]
    row['topic_name_top'] = translated_topic_names_top[thread_id]
    row['topic_name_leaf'] = translated_topic_names_leaf[thread_id]
    
    # Translate the thread_text field
    row['thread_text'] = translate(row['thread_text'], tokenizer, model, device)
    
    # Add the processed row to the list
    processed_rows.append(row)
    
    

# Write any remaining rows to CSV
if processed_rows:
    write_chunk_to_csv(pd.DataFrame(processed_rows), output_file, mode='a')

print(f"Translation complete! The translated CSV is saved as {output_file}.")
