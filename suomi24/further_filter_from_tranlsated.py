import pandas as pd

# Load CSV files into pandas DataFrames
df_a = pd.read_csv("C:/Users/fahad/OneDrive/Documents/Thesis/suomi24/Data/further_filtered/s24_2004.csv")
df_b = pd.read_csv("C:/Users/fahad/OneDrive/Documents/Thesis/suomi24/Data/filtered_translated/s24_2004.csv")

# Filter rows in df_b based on thread_id present in df_a
filtered_df_b = df_b[df_b['thread_id'].isin(df_a['thread_id'])]

# Save the filtered DataFrame to a new CSV file
filtered_df_b.to_csv("C:/Users/fahad/OneDrive/Documents/Thesis/suomi24/Data/further_filtered_translated/s24_2004.csv", index=False)


