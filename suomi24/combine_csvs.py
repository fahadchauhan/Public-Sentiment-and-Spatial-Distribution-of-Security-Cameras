import pandas as pd
import os
import re

# Step 1: Combine all CSV files into one DataFrame
path = 'C:/Users/fahad/OneDrive - Oulun yliopisto/Documents/suomi24/Data/further_filtered_translated/'  # Directory where CSV files are stored
all_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.csv')]

df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

print("joined")

# Step 2: Preprocess text using the updated clean_text function
def clean_text(text):
    # Replace specific character sequences and keep only ASCII characters (including punctuation)
    text = text.replace('â€™', "'")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

# Columns to preprocess
columns_to_process = ['title', 'topic_name_top', 'topic_name_leaf', 'thread_text']

for column in columns_to_process:
    df[column] = df[column].astype(str).apply(clean_text)

print("cleaned")
# Step 3: Remove duplicates within the same row for each column that might contain sentences
def remove_duplicate_sentences(text):
    sentences = re.split(r'(?<=[.])\s*', text)
    unique_sentences = set(sentences)
    text = ' '.join(sentence.strip() for sentence in unique_sentences if sentence.strip())
    
    sentences = re.split(r'(?<=[?])\s*', text)
    unique_sentences = set(sentences)
    text = ' '.join(sentence.strip() for sentence in unique_sentences if sentence.strip())

    sentences = re.split(r'(?<=[,])\s*', text)
    unique_sentences = set(sentences)
    text = ' '.join(sentence.strip() for sentence in unique_sentences if sentence.strip())

    sentences = re.split(r'(?<=[!])\s*', text)
    unique_sentences = set(sentences)
    text = ' '.join(sentence.strip() for sentence in unique_sentences if sentence.strip())
    return text

for column in columns_to_process:
    df[column] = df[column].apply(remove_duplicate_sentences)

print("removed")
# Save the combined and cleaned DataFrame to a new CSV file
df.to_csv('suomi24/Data/suomi24.csv', index=False)
