import pandas as pd
import re
from tqdm import tqdm

input_file = "C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/reddit_clean.csv"
output_file = "C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/reddit_clean.csv"

# Define a list of phrases where each phrase is a list of words that need to be present in any order
phrases = [
    ["public", "camera", "privacy"],
    ["cctv", "surveill"],
    ["camera", "surveill"],
    ["security", "camera"],
    ["public", "safety", "concern"],
    ["public", "security", "concern"],
    ["monitor", "cctv"],
    ["monitor", "camera"],
    ["public", "footage"],
    ["camera", "footage"],
    ["street", "camera"],
]

# Compile regular expressions for each word in the phrases to allow flexible matching
compiled_phrases = [
    [re.compile(r'\b' + re.escape(word) + r'\w*\b', re.IGNORECASE) for word in phrase]
    for phrase in phrases
]

# Function to check if text contains all words of any phrase in any order
def contains_all_words_of_any_phrase(text):
    if pd.isna(text):
        return False
    for phrase in compiled_phrases:
        if all(pattern.search(text) for pattern in phrase):
            return True
    return False

# Load the combined CSV file
df = pd.read_csv(input_file, dtype={'thread_id': str, 'comment_id': str})

tqdm.pandas(desc="Processing")
print("identify keys")
# Identify rows with keywords in 'title' or 'thread_text'
df['has_keyword'] = df['title'].progress_apply(contains_all_words_of_any_phrase) | df['thread_text'].progress_apply(contains_all_words_of_any_phrase)


# Identify thread_ids with keywords
thread_ids_with_keywords = set(df[df['has_keyword']]['thread_id'])

print("filter rows")
# Filter rows: keep rows where thread_id is in thread_ids_with_keywords
df_filtered = df[df['thread_id'].isin(thread_ids_with_keywords)].copy()

print("remoce non comment submissions")
# Remove submissions with no comments
df_filtered = df_filtered.groupby('thread_id').filter(lambda x: (x['msg_type'] == 'comment').any())

print("count comments")
# Count comments per thread_id
comment_counts = df_filtered[df_filtered['msg_type'] == 'comment'].groupby('thread_id').size()

print("keep valid posts")
# Identify thread_ids with at least 3 comments
valid_thread_ids = comment_counts[comment_counts >= 3].index

print("filter rows")
# Filter out posts with fewer than 3 comments
df_final_filtered = df_filtered[df_filtered['thread_id'].isin(valid_thread_ids)].copy()

# Drop the temporary 'has_keyword' column
df_filtered.drop(columns=['has_keyword'], inplace=True)

print("writing csv")
# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(output_file, index=False, encoding='utf-8', lineterminator='\n')

# Print the first few rows of the filtered DataFrame
print(df_filtered)
