import pandas as pd
import os

# Path to the directory containing your CSV files
csv_directory = 'C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/'

# List of CSV files to combine
csv_files = ['2023-01.csv', '2023-02.csv', 'AskEurope.csv', 'AskReddit.csv', 'privacy.csv', 'security.csv', 'technology.csv']

# Initialize an empty list to store dataframes
dataframes = []

# Read each CSV file and append to the list
for csv_file in csv_files:
    file_path = os.path.join(csv_directory, csv_file)
    df = pd.read_csv(file_path)
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('C:/Users/fahad/OneDrive/Documents/Thesis/reddit/Data/filtered/reddit.csv', index=False)
