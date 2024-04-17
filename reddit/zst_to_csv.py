# this converts a zst file to csv
#
# it's important to note that the resulting file will likely be quite large
# and you probably won't be able to open it in excel or another csv reader
#
# arguments are inputfile, outputfile, fields
# call this like
# python to_csv.py wallstreetbets_submissions.zst wallstreetbets_submissions.csv author,selftext,title

import zstandard
import os
import json
import sys
import csv
from datetime import datetime
import logging.handlers


# put the path to the input file
# input_file_path = "reddit/Data/non-filtered/RS_2023-03.zst"
# put the path to the output file, with the csv extension
# output_file_path = "reddit/Data/non-filtered/RS_2023-03.csv"
# if you want a custom set of fields, put them in the following list. If you leave it empty the script will use a default set of fields

input_file_path = "D:/Thesis/reddit/comments/RC_2023-01.zst"
output_file_path = "D:/Thesis/reddit/comments/RC_2023-01.csv"

fields = []

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		print("buffer")
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		print(f"reader done")
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)
			
			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line, file_handle.tell()

			buffer = lines[-1]
		print(f"while done")
		reader.close()


if __name__ == "__main__":
	if len(sys.argv) >= 3:
		input_file_path = sys.argv[1]
		output_file_path = sys.argv[2]
		fields = sys.argv[3].split(",")

	is_submission = "submission" in input_file_path
	if not len(fields):
		if is_submission:
			fields = ["author","title","score","created","link","text","url"]
		else:
			fields = ["author","score","created","link","body"]

	file_size = os.stat(input_file_path).st_size
	file_lines, bad_lines = 0, 0
	line, created = None, None
	output_file = open(output_file_path, "w", encoding='utf-8', newline="")
	writer = csv.writer(output_file)
	writer.writerow(fields)
	try:
		for line, file_bytes_processed in read_lines_zst(input_file_path):
			# print("\nerror")
			try:
				# print("try")
				obj = json.loads(line)
				# print("json loads line")
				output_obj = []
				for field in fields:
					if field == "created":
						value = datetime.fromtimestamp(int(obj['created_utc'])).strftime("%Y-%m-%d %H:%M")
					elif field == "link":
						if 'permalink' in obj:
							value = f"https://www.reddit.com{obj['permalink']}"
						else:
							value = f"https://www.reddit.com/r/{obj['subreddit']}/comments/{obj['link_id'][3:]}/_/{obj['id']}/"
					elif field == "author":
						value = f"u/{obj['author']}"
					elif field == "text":
						if 'selftext' in obj:
							value = obj['selftext']
						else:
							value = ""
					else:
						value = obj[field]

					output_obj.append(str(value).encode("utf-8", errors='replace').decode())
				# print("for fields end")
				writer.writerow(output_obj)

				created = datetime.utcfromtimestamp(int(obj['created_utc']))
				# print("datetime created")
			except json.JSONDecodeError as err:
				bad_lines += 1
			file_lines += 1
			# print("file_lines +1")
			if file_lines % 1000000 == 0:
				log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {file_lines:,} : {bad_lines:,} : {(file_bytes_processed / file_size) * 100:.0f}%")
				# print("printing if")
			# print("not printing if")
	except KeyError as err:
		log.info(f"Object has no key: {err}")
		log.info(f"line: {line}")
	except Exception as err:
		log.info(f"exception: {err}")
		log.info(f"line: {line}")
	# print("exception ran close file")
	output_file.close()
	log.info(f"Complete : {file_lines:,} : {bad_lines:,}")
