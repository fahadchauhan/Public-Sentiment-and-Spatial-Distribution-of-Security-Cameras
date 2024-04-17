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

input_file_path = "D:/Thesis/reddit/comments/RC_2023-02.zst"
output_file_path = "D:/Thesis/reddit/comments/RC_2023-02.csv"

fields = []

dic = {"all_awardings":[],"archived":"false","associated_award":"null","author":"Pouletchien","author_created_utc":"1532892027","author_flair_background_color":"","author_flair_css_class":"sheet6-col08-row07","author_flair_richtext":[{"e":"text","t":"MTL - NHL "},{"a":":60807:","e":"emoji","u":"https:\/\/emoji.redditmedia.com\/rsxzgwn08xl91_t5_2qiel\/60807"}],"author_flair_template_id":"null","author_flair_text":"MTL - NHL :60807:","author_flair_text_color":"dark","author_flair_type":"richtext","author_fullname":"t2_1vo7xzab","author_patreon_flair":"false","author_premium":"false","body":"Someone that knows Football explain to me how it is incomplete. \n\nThe ball is in his hand caught before he get hit. If he doesn’t get hit, it doesn’t fall off his hand.","can_gild":"true","collapsed":"false","collapsed_because_crowd_control":"null","collapsed_reason":"null","collapsed_reason_code":"null","comment_type":"null","controversiality":0,"created_utc":1676253906,"distinguished":"null","edited":"false","gilded":0,"gildings":{},"id":"j8bhf0f","is_submitter":"false","link_id":"t3_110swd4","locked":"false","name":"t1_j8bhf0f","no_follow":"false","parent_id":"t3_110swd4","permalink":"\/r\/hockey\/comments\/110swd4\/game_thread_philadelphia_eagles_vs_kansas_city\/j8bhf0f\/","retrieved_on":"1678222579","score":4,"score_hidden":"false","send_replies":"true","stickied":"false","subreddit":"hockey","subreddit_id":"t5_2qiel","subreddit_name_prefixed":"r\/hockey","subreddit_type":"public","top_awarded_type":"null","total_awards_received":"0","treatment_tags":[],"unrepliable_reason":"null"}

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
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)
			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line, file_handle.tell()

			buffer = lines[-1]
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
			line = dic
			try:
				obj = json.loads(line)
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
				writer.writerow(output_obj)

				created = datetime.utcfromtimestamp(int(obj['created_utc']))
				break
			except json.JSONDecodeError as err:
				bad_lines += 1
			file_lines += 1
			if file_lines % 100000 == 0:
				log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {file_lines:,} : {bad_lines:,} : {(file_bytes_processed / file_size) * 100:.0f}%")
                
	except KeyError as err:
		log.info(f"Object has no key: {err}")
		log.info(f"line: {line}")
	except Exception as err:
		log.info(f"exception: {err}")
		log.info(f"line: {line}")

	output_file.close()
	log.info(f"Complete : {file_lines:,} : {bad_lines:,}")
