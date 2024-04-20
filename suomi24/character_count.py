import pandas as pd

def count_characters_in_csv(file_path, columns):
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
        
        # Calculate the total number of characters across specified columns
        total_characters = 0
        for column in columns:
            # Sum the number of characters in each cell of the column
            character_count = df[column].astype(str).apply(len).sum()
            total_characters += character_count
        return total_characters
    except FileNotFoundError:
        print(f"No file found at {file_path}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

# Base directory and file pattern
base_path = 'Data/filtered/s24_{}.csv'

# Specify the columns you want to count characters in
columns_to_count = ['title', 'topic_name_top', 'thread_text']

# Specify the range of years
start_year = 2001
end_year = 2020

# Variable to hold the cumulative sum of characters
cumulative_characters = 0

# Loop over each year and process the respective file
for year in range(start_year, end_year + 1):
    file_path = base_path.format(year)
    year_characters = count_characters_in_csv(file_path, columns_to_count)
    print(f"Total characters in {year}: {year_characters}")
    cumulative_characters += year_characters

print(f"Total characters from {start_year} to {end_year}: {cumulative_characters}")
