import pandas as pd

# Load the CSV files
subreddit = "technology"
submissions_file = f'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/{subreddit}_submissions.csv'
comments_file = f'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/{subreddit}_comments.csv'

df_submissions = pd.read_csv(submissions_file)
df_comments = pd.read_csv(comments_file)

# Add missing columns in submissions and comments
df_submissions['comment_id'] = 0
df_comments['title'] = df_comments['thread_id'].map(df_submissions.set_index('thread_id')['title'])

# If thread_id doesn't exist in submissions, leave the title empty
df_comments['title'] = df_comments['title'].fillna('')

# Concatenate the dataframes
combined_df = pd.concat([df_submissions, df_comments], ignore_index=True)

# Reorder the columns
columns_order = ['subreddit', 'msg_type', 'score', 'link', 'author', 'datetime', 'title', 'thread_id', 'comment_id', 'thread_text']
combined_df = combined_df[columns_order]

print(combined_df.head())

# Save the combined dataframe to a new CSV file
combined_df.to_csv(f'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/{subreddit}.csv', index=False)
