import pandas as pd
import re

from tqdm import tqdm

submissions_input_file = "D:/Thesis/reddit/submissions/RS_2023-02.csv"
submissions_output_file = 'reddit/Data/filtered/RS_2023-02.csv'

comments_input_file = "D:/Thesis/reddit/comments/RC_2023-02.csv"
comments_output_file = 'reddit/Data/filtered/RC_2023-02.csv'

# Define a list of phrases where each phrase is a list of words that need to be present in any order
phrases = [
    ["CCTV"],
    ["public", "cameras"],
    ["surveillance"],
    ["security", "cameras"],
    ["public", "safety"],
    ["privacy"],
    ["security", "concern"],
    ["data", "protection"],
    ["civil", "liberties"],
    ["Big", "Brother"],
    ["monitoring"],
    ["camera", "surveillance"],
    ["urban", "surveillance"],
    ["public", "footage"],
    ["camera", "footage"],
    ["CCTV", "safety"],
    ["street", "cameras"]
]

# phrases = [
#     ["cctv"],
#     ["public", "camera"],
#     ["surveill"],
#     ["security", "camera"],
#     ["public", "safety"],
#     ["privacy"],
#     ["security", "concern"],
#     ["data", "protect"],
#     ["civil", "libert"],
#     ["big", "brother"],
#     ["monitor"],
#     ["public", "footage"],
#     ["camera", "footage"],
#     ["cctv", "safety"],
#     ["street", "camera"]
# ]
# Compile regular expressions for each word in the phrases to allow flexible matching
compiled_phrases = [
    [re.compile(r'\b' + re.escape(word) + r'\w*\b', re.IGNORECASE) for word in phrase]
    for phrase in phrases
]

# print(f"compiled_phrases: {compiled_phrases}")
# Function to check if text contains all words of any phrase in any order
def contains_any_phrase(text):
    if pd.isna(text):
        return False
    for phrase in compiled_phrases:
        if all(pattern.search(text) for pattern in phrase):
            return True
    return False

# Initialize sets to keep track of identifiers
submission_identifiers_with_keywords = set()
new_comment_identifiers_with_keywords = set()

# Open the output files once and keep writing to them
with open(submissions_output_file, 'w', encoding='utf-8') as f_subs, open(comments_output_file, 'w', encoding='utf-8') as f_coms:
    # Process submissions
    first_sub_chunk = True
    first_com_chunk = True
    for chunk in tqdm(pd.read_csv(submissions_input_file, chunksize=100000)):
        chunk['has_keyword'] = chunk['title'].apply(contains_any_phrase) | chunk['text'].apply(contains_any_phrase)
        chunk['key'] = chunk['link'].apply(lambda x: re.search(r'/comments/(\w+)/', x).group(1) if re.search(r'/comments/(\w+)/', x) else None)
        filtered_chunk = chunk[chunk['has_keyword']].copy()
        submission_identifiers_with_keywords.update(filtered_chunk['key'])
        if not filtered_chunk.empty:
            filtered_chunk.drop(columns=["has_keyword"])
            filtered_chunk.to_csv(f_subs, mode='a', index=False, header=first_sub_chunk, encoding='utf-8', lineterminator='\n')
            first_sub_chunk = False
        # break

    # Process comments
    for chunk in tqdm(pd.read_csv(comments_input_file, chunksize=100000)):
        chunk['has_keyword'] = chunk['body'].apply(contains_any_phrase)
        chunk['key'] = chunk['link'].apply(lambda x: re.search(r'/comments/(\w+)/', x).group(1) if re.search(r'/comments/(\w+)/', x) else None)
        comments_with_keywords = chunk[chunk['has_keyword']].copy()
        new_comment_identifiers_with_keywords.update(comments_with_keywords['key'])
        relevant_comments = chunk[chunk['key'].isin(submission_identifiers_with_keywords)].copy()
        comments_to_keep = pd.concat([comments_with_keywords, relevant_comments], ignore_index=True).drop_duplicates()
        if not comments_to_keep.empty:
            comments_to_keep.drop(columns=["has_keyword"])
            comments_to_keep.to_csv(f_coms, mode='a', index=False, header=first_com_chunk, encoding='utf-8', lineterminator='\n')
            first_com_chunk = False

    # Additional submissions from new comment identifiers
    new_identifiers = new_comment_identifiers_with_keywords - submission_identifiers_with_keywords
    if new_identifiers:
        for chunk in tqdm(pd.read_csv(submissions_input_file, chunksize=100000)):
            chunk['key'] = chunk['link'].apply(lambda x: re.search(r'/comments/(\w+)/', x).group(1) if re.search(r'/comments/(\w+)/', x) else None)
            additional_chunk = chunk[chunk['key'].isin(new_identifiers)].copy()
            if not additional_chunk.empty:
                additional_chunk.to_csv(f_subs, mode='a', index=False, header=first_sub_chunk, encoding='utf-8', lineterminator='\n')
