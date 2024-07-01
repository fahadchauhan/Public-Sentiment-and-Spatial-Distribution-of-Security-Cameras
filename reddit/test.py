import pandas as pd








# # Load the CSV files
# submissions_file = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-01.csv'

# df_submissions = pd.read_csv(submissions_file)

# # Identify and remove duplicate thread_id values in df_submissions
# df_submissions_no_duplicates = df_submissions.drop_duplicates(subset='thread_id', keep=False)

# print("Original number of rows:", len(df_submissions))
# print("Number of rows after removing duplicates:", len(df_submissions_no_duplicates))

# # Save the cleaned DataFrame back to a CSV file if needed
# df_submissions_no_duplicates.to_csv('C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-01-noDuplicates.csv', index=False)


# # Load the CSV files
submissions_file = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-02.csv'

df_submissions = pd.read_csv(submissions_file)

duplicate_thread_ids = df_submissions[df_submissions.duplicated(subset='thread_id', keep=False)]
print("Duplicate thread_ids in df_submissions:")
print(duplicate_thread_ids[["subreddit", "score", "link", "author", "thread_id", "thread_text"]])




# import pandas as pd

# # Load your data
# file_path = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-02.csv'


# df_comments = pd.read_csv(file_path)

# # Function to extract the thread ID from the URL
# def extract_thread_id(link):
#     parts = link.split('/')
#     for i, part in enumerate(parts):
#         if part == 'comments':
#             if i + 1 < len(parts):
#                 return parts[i + 1]
#     return ''

# # Apply the function to extract thread IDs
# df_comments['thread_id'] = df_comments['link'].apply(extract_thread_id)

# # Save the updated DataFrame to a new CSV
# df_comments.to_csv('C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-02.csv', index=False)


# file_path = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/AskReddit_comments-updated.csv'
# df = pd.read_csv(file_path)
# print(df[df['comment_id']=='c81hm9c'])