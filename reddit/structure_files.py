import pandas as pd
import re


# Submissions files

# # Load your data
# file_path = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-02.csv'
# df = pd.read_csv(file_path)
# print(df.head())
# # Rename columns
# df.rename(columns={
#     'created': 'datetime',
#     'key': 'thread_id',
#     'text': 'thread_text'
# }, inplace=True)

# # Add new columns
# df['msg_type'] = 'thread_start'

# # Extract subreddit from link
# df['subreddit'] = df['link'].apply(lambda x: x.split('/r/')[1].split('/')[0] if '/r/' in x else '')

# # Reorder columns with subreddit at the start
# new_column_order = ['subreddit', 'msg_type', 'score', 'link', 'url', 'author', 'datetime', 'title', 'thread_id', 'thread_text']
# df = df[new_column_order]

# # Save the updated DataFrame to a CSV file
# output_file_path = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RS_2023-02-updated.csv'
# df.to_csv(output_file_path, index=False)

# # Print the DataFrame to check
# print(df.head())

# Comments Files

# # Load the data
# file_path = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RC_2023-02.csv'
# df = pd.read_csv(file_path)
# print(df.head())
# # Add and fill 'msg_type' column with 'comment'
# df['msg_type'] = 'comment'

# # Change 'created' to 'datetime'
# df.rename(columns={'created': 'datetime', 'body': 'thread_text', 'key': 'thread_id'}, inplace=True)

# # Extract 'comment_id' from the 'link'
# df['comment_id'] = df['link'].apply(lambda x: x.split('/')[-2] if '/' in x else x)

# # Create 'subreddit' column from the 'link'
# df['subreddit'] = df['link'].apply(lambda x: x.split('/r/')[1].split('/')[0] if '/r/' in x else '')

# # Reorder the columns
# df = df[['subreddit', 'msg_type', 'score', 'link', 'author', 'datetime', 'thread_id', 'comment_id', 'thread_text']]

# # Save the transformed dataframe
# df.to_csv('C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/RC_2023-02-updated.csv', index=False)

# # Display the first few rows to confirm changes
# print(df.head())
