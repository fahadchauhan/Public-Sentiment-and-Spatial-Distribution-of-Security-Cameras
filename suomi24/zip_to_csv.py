import os
import zipfile
import re
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
import time

# Function to append data to a file
def append_to_file(data, filename):
    # Check if file exists to write headers
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    while True:
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerows(data)
            break
        except Exception as e:
            print(e)
            print(f"Error in writing file {filename}!")
            time.sleep(5)


def extract_vrt_data_from_chunk(chunk):
    # Extract attributes of <text> element
    msg_type = re.search(r'msg_type="(.*?)"', chunk).group(1)
    datetime = re.search(r'datetime="(.*?)"', chunk).group(1)
    title = re.search(r'title="(.*?)"', chunk).group(1)
    thread_id = re.search(r'thread_id="(.*?)"', chunk).group(1)
    comment_id = re.search(r'comment_id="(.*?)"', chunk).group(1)
    topic_name_top = re.search(r'topic_name_top="(.*?)"', chunk).group(1)
    topic_name_leaf = re.search(r'topic_name_leaf="(.*?)"', chunk).group(1)

    # Extract sentences
    sentences = re.findall(r'<sentence(.*?)</sentence>', chunk, re.DOTALL)
    thread_text = ' '.join([' '.join(re.findall(r'^(\S+?)\t', sentence, re.MULTILINE)) for sentence in sentences])

    return {
        'msg_type': msg_type,
        'datetime': datetime,
        'title': title,
        'thread_id': thread_id,
        'comment_id': comment_id,
        'topic_name_top': topic_name_top,
        'topic_name_leaf': topic_name_leaf,
        'thread_text': thread_text,
    }

def process_single_vrt_file(zip_ref, vrt_file, output_folder, num_messages, vrt_count, zip_filename):
    # if vrt_file.split("/")[-1] in ['s24_2001.vrt', 's24_2002.vrt', 's24_2003.vrt']:
    #     return
    output_file = os.path.join(output_folder, f's24_{vrt_count}.csv')
    with zip_ref.open(vrt_file, 'r') as file:
        print(f"{vrt_file} started!")
        chunk = ""
        entries = []  # List to collect dictionaries
        for line in file:
            line = line.decode('utf-8', errors='replace')
            chunk += line
            if '</text>' in line:
                entry = extract_vrt_data_from_chunk(chunk)
                entries.append(entry)
                chunk = ""
                if len(entries) >= num_messages:  # Write to file once we have 5000 entries
                    append_to_file(entries, output_file)
                    print(f"{num_messages} number of messages Done from {zip_filename}/{vrt_file}!")
                    entries = []  # Reset the list
                elif len(entries)%(num_messages/5)==0:
                    print(f"{len(entries)} number of messages Done from {zip_filename}/{vrt_file}!")

        # Write any remaining entries to the file
        if entries:
            append_to_file(entries, output_file)
                # count += 1


def process_zip_files(zip_filenames, output_folder, num_messages, max_threads=8):
# with ThreadPoolExecutor(max_workers=max_workers) as executor:
    threads = []
    # vrt_count = 0
    for zip_filename in zip_filenames:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            # Submit each .vrt file to the thread pool for processing
            for vrt_file in zip_ref.namelist():
                if vrt_file.endswith('.vrt'):
                    # vrt_count += 1

                    pattern = r'\d{4}'
                    matches = re.findall(pattern, vrt_file)
                    if matches:
                        vrt_count = matches[-1]

                    thread = threading.Thread(target=process_single_vrt_file, args=(zip_ref, vrt_file, output_folder, num_messages, vrt_count, zip_filename))
                    threads.append(thread)
                    thread.start()
                    # executor.submit(process_single_vrt_file, zip_ref, vrt_file, output_folder, num_messages, vrt_count, zip_filename)
                    # If we've reached the max number of threads, wait for all of them to finish before starting more
                    if len(threads) == max_threads:
                        for t in threads:
                            t.join()
                        threads = []

    # Wait for any remaining threads to finish
    for t in threads:
        t.join()
                            
# Paths and parameters
zip_files = ['Data/suomi24/2001-2017/suomi24-2001-2017-vrt-v1-2.zip']
output_folder = 'Data/suomi24/2001-2020'
num_messages = 100000  # Change this to the number of messages you want to parse per file

# Process the zip files
process_zip_files(zip_files, output_folder, num_messages, max_threads=8)

print("Done!")