import pandas as pd
import re
from tqdm import tqdm

chunk_size = 50000  # Number of rows per chunk
# filenames = ["suomi24/Data/2001-2020/s24_2008.csv", "suomi24/Data/2001-2020/s24_2009.csv", "suomi24/Data/2001-2020/s24_2010.csv", "suomi24/Data/2001-2020/s24_2011.csv", "suomi24/Data/2001-2020/s24_2012.csv", "suomi24/Data/2001-2020/s24_2013.csv", "suomi24/Data/2001-2020/s24_2014.csv", "suomi24/Data/2001-2020/s24_2015.csv", "suomi24/Data/2001-2020/s24_2016.csv", "suomi24/Data/2001-2020/s24_2017.csv", "suomi24/Data/2001-2020/s24_2018.csv", "suomi24/Data/2001-2020/s24_2019.csv", "suomi24/Data/2001-2020/s24_2020.csv"]
# output_files = ["suomi24/Data/filtered/s24_2008.csv", "suomi24/Data/filtered/s24_2009.csv", "suomi24/Data/filtered/s24_2010.csv", "suomi24/Data/filtered/s24_2011.csv", "suomi24/Data/filtered/s24_2012.csv", "suomi24/Data/filtered/s24_2013.csv", "suomi24/Data/filtered/s24_2014.csv", "suomi24/Data/filtered/s24_2015.csv", "suomi24/Data/filtered/s24_2016.csv", "suomi24/Data/filtered/s24_2017.csv", "suomi24/Data/filtered/s24_2018.csv", "suomi24/Data/filtered/s24_2019.csv", "suomi24/Data/filtered/s24_2020.csv"]

# filenames = ["suomi24/Data/filtered/s24_2001.csv", "suomi24/Data/filtered/s24_2002.csv", "suomi24/Data/filtered/s24_2003.csv", "suomi24/Data/filtered/s24_2004.csv", "suomi24/Data/filtered/s24_2005.csv", "suomi24/Data/filtered/s24_2007.csv", "suomi24/Data/filtered/s24_2008.csv", "suomi24/Data/filtered/s24_2009.csv", "suomi24/Data/filtered/s24_2010.csv", "suomi24/Data/filtered/s24_2011.csv", "suomi24/Data/filtered/s24_2012.csv", "suomi24/Data/filtered/s24_2013.csv", "suomi24/Data/filtered/s24_2014.csv", "suomi24/Data/filtered/s24_2015.csv", "suomi24/Data/filtered/s24_2016.csv", "suomi24/Data/filtered/s24_2017.csv", "suomi24/Data/filtered/s24_2018.csv", "suomi24/Data/filtered/s24_2019.csv", "suomi24/Data/filtered/s24_2020.csv"]
# output_files = ["suomi24/Data/further_filtered/s24_2001.csv", "suomi24/Data/further_filtered/s24_2002.csv", "suomi24/Data/further_filtered/s24_2003.csv", "suomi24/Data/further_filtered/s24_2004.csv", "suomi24/Data/further_filtered/s24_2005.csv", "suomi24/Data/further_filtered/s24_2007.csv", "suomi24/Data/further_filtered/s24_2008.csv", "suomi24/Data/further_filtered/s24_2009.csv", "suomi24/Data/further_filtered/s24_2010.csv", "suomi24/Data/further_filtered/s24_2011.csv", "suomi24/Data/further_filtered/s24_2012.csv", "suomi24/Data/further_filtered/s24_2013.csv", "suomi24/Data/further_filtered/s24_2014.csv", "suomi24/Data/further_filtered/s24_2015.csv", "suomi24/Data/further_filtered/s24_2016.csv", "suomi24/Data/further_filtered/s24_2017.csv", "suomi24/Data/further_filtered/s24_2018.csv", "suomi24/Data/further_filtered/s24_2019.csv", "suomi24/Data/further_filtered/s24_2020.csv"]

filenames = ["suomi24/Data/filtered/s24_2005.csv", "suomi24/Data/filtered/s24_2007.csv", "suomi24/Data/filtered/s24_2008.csv", "suomi24/Data/filtered/s24_2009.csv", "suomi24/Data/filtered/s24_2010.csv", "suomi24/Data/filtered/s24_2011.csv", "suomi24/Data/filtered/s24_2012.csv", "suomi24/Data/filtered/s24_2013.csv", "suomi24/Data/filtered/s24_2014.csv", "suomi24/Data/filtered/s24_2015.csv", "suomi24/Data/filtered/s24_2016.csv", "suomi24/Data/filtered/s24_2017.csv", "suomi24/Data/filtered/s24_2018.csv", "suomi24/Data/filtered/s24_2019.csv", "suomi24/Data/filtered/s24_2020.csv"]
output_files = ["suomi24/Data/further_filtered/s24_2005.csv", "suomi24/Data/further_filtered/s24_2007.csv", "suomi24/Data/further_filtered/s24_2008.csv", "suomi24/Data/further_filtered/s24_2009.csv", "suomi24/Data/further_filtered/s24_2010.csv", "suomi24/Data/further_filtered/s24_2011.csv", "suomi24/Data/further_filtered/s24_2012.csv", "suomi24/Data/further_filtered/s24_2013.csv", "suomi24/Data/further_filtered/s24_2014.csv", "suomi24/Data/further_filtered/s24_2015.csv", "suomi24/Data/further_filtered/s24_2016.csv", "suomi24/Data/further_filtered/s24_2017.csv", "suomi24/Data/further_filtered/s24_2018.csv", "suomi24/Data/further_filtered/s24_2019.csv", "suomi24/Data/further_filtered/s24_2020.csv"]

# Define your stemmed keyword phrases and compile the regex patterns outside the loop
phrases = [
    ["public", "camera", "privacy"],
    ["public", "camera", "yksityisyyttä"],
    ["public", "camera", "yksity"],
    ["julkinen", "kamera", "yksityisyyttä"],
    ["julkinen", "camera", "yksityisyyttä"],
    ["julkinen", "kamera", "yksity"],
    ["julkinen", "camera", "yksity"],
    ["cctv", "surveill"],
    ["cctv", "valvontaa"],
    ["cctv", "valvo"],
    ["camera", "surveill"],
    ["kamera", "surveill"],
    ["camera", "valvontaa"],
    ["kamera", "valvontaa"],
    ["camera", "valvo"],
    ["kamera", "valvo"],
    ["security", "camera"],
    ["turvatoimet", "camera"],
    ["turvatoimet", "kamera"],
    ["public", "safety", "concern"],
    ["julkinen", "turvallisuus", "koskea"],
    ["julkinen", "turvallisuus", "huole"],
    ["public", "security", "concern"],
    ["julkinen", "turvatoimet", "koskea"],
    ["julkinen", "turvatoimet", "huole"],
    ["monitor", "cctv"],
    ["seurantaa", "cctv"],
    ["seurant", "cctv"],
    ["monitor", "camera"],
    ["seurantaa", "camera"],
    ["seurant", "camera"],
    ["monitor", "kamera"],
    ["seurantaa", "kamera"],
    ["seurant", "kamera"],
    ["public", "footage"],
    ["julkinen", "kuvamateriaali"],
    ["camera", "footage"],
    ["camera", "kuvamateriaali"],
    ["kamera", "kuvamateriaali"],
    ["street", "camera"],
    ["katu", "camera"],
    ["katu", "kamera"]
]

# phrases = [
#     ["cctv"],
#     ["public", "camera"],
#     ["julkinen", "kamera"],
#     ["julkinen", "camera"],
#     ["surveill"],
#     ["valvontaa"],
#     ["valvo"],
#     ["security", "camera"],
#     ["turvatoimet", "camera"],
#     ["turvatoimet", "kamera"],
#     ["public", "safety"],
#     ["julkinen", "turvallisuus"],
# 	["privacy"],
#     ["yksityisyyttä"],
#     ["yksity"],
#     ["security", "concern"],
#     ["turvatoimet", "koskea"],
#     ["turvatoimet", "huole"],
#     ["data", "protect"],
#     ["data", "suoj"],
#     ["tieto", "suoj"],
#     ["civil", "libert"],
#     ["sivi", "vapautta"],
#     ["sivi", "vapau"],
#     ["big", "brother"],
#     ["monitor"],
#     ["seurantaa"],
#     ["seurant"],
#     ["public", "footage"],
#     ["julkinen", "kuvamateriaali"],
#     ["camera", "footage"],
#     ["camera", "kuvamateriaali"],
#     ["kamera", "kuvamateriaali"],
#     ["street", "camera"],
#     ["katu", "camera"],
#     ["katu", "kamera"]
# ]

# Compile the regex patterns allowing for different suffixes based on the stem
patterns = [
    [re.compile(r'\b' + re.escape(word) + r'\w*\b', re.IGNORECASE) for word in phrase]
    for phrase in phrases
]

# Function to check if any given row matches all the keyword phrases
def check_row_for_phrases(row, patterns):
    combined_text = f"{row['title']} {row['topic_name_top']} {row['thread_text']}".lower()
    # Check for each phrase if all patterns in the phrase are found in the combined text
    return any(all(pattern.search(combined_text) for pattern in phrase_patterns) for phrase_patterns in patterns)

for filename,output_file in zip(filenames,output_files):
    print(f"filename: {filename}")
    # Initialize the CSV file (ensure it's empty and has the appropriate headers)
    with pd.read_csv(filename, chunksize=1) as reader:  # read the first row to get column names
        first_row = next(reader)
        pd.DataFrame(columns=first_row.columns).to_csv(output_file, index=False)

    # Variable to keep track of the current thread ID and whether it should be retained
    current_thread_id = None
    retain_current_thread = False
    results_to_write = []  # This will store all rows to write from the current chunk

    # total_rows = sum(1 for _ in pd.read_csv(filename, chunksize=chunk_size))
    # print(f"total_rows: {total_rows}")
    # file_lines = 0

    count = 0
    # Process the data in a single pass
    for chunk in tqdm(pd.read_csv(filename, chunksize=chunk_size)):
        results = []
        count += 1
        for index, row in chunk.iterrows():
            # file_lines += 1
            if row['thread_id'] != current_thread_id:
                # If moving to a new thread, write results if the previous thread was to be retained
                if retain_current_thread:
                    results_to_write.extend(results)
                # Reset for the new thread
                current_thread_id = row['thread_id']
                retain_current_thread = False
                results = []

            # Append row to results (it will be added to results_to_write if this thread is retained)
            results.append(row)

            # Check if the current row matches the keywords
            if not retain_current_thread:  # Only check for matches if the thread hasn't been flagged yet
                if check_row_for_phrases(row, patterns):
                    retain_current_thread = True

        # Ensure the last tracked thread in the chunk is also written if needed
        if retain_current_thread:
            results_to_write.extend(results)

        # Write all accumulated results to the CSV file
        if results_to_write:
            pd.DataFrame(results_to_write).to_csv(output_file, mode='a', header=False, index=False)
            results_to_write = []  # Clear the list after writing
            # print(f"{(file_lines / total_rows) * 100:.2f}% of data processed.")
        
        # if count==3:
        #     break

print("Data processing complete. Filtered data written to", output_file)
