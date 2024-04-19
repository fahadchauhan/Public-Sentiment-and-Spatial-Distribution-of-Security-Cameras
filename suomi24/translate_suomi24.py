import pandas as pd
from googletrans import Translator

def translate_text(text, src_lang='fi', dest_lang='en'):
    translator = Translator()
    try:
        translation = translator.translate(text, src=src_lang, dest=dest_lang)
        return translation.text
    except Exception as e:
        print(f"Error during translation: {e} on text: {text}")
        return text

def process_translate_chunk(chunk, columns):
    # Concatenate the specified columns with a unique delimiter
    chunk['combined'] = chunk[columns].apply(lambda x: ' ||| '.join(x.map(str)), axis=1)
    # Translate the concatenated text
    chunk['combined'] = chunk['combined'].apply(translate_text)
    # Split the translated text back into the original columns
    new_columns = chunk['combined'].str.split(' ||| ', expand=True)
    for i, column in enumerate(columns):
        chunk[column] = new_columns[i]
    return chunk.drop(columns=['combined'])

def translate_dataframe_in_chunks(df, columns, chunk_size=200000):
    output_file = 'suomi24/Data/translated/s24_2001.csv'
    first_chunk = True
    for start in range(0, df.shape[0], chunk_size):
        chunk = df.iloc[start:start + chunk_size]
        translated_chunk = process_translate_chunk(chunk, columns)
        # Write each chunk to CSV, header only in the first chunk
        translated_chunk.to_csv(output_file, mode='a', header=first_chunk, index=False)
        first_chunk = False
        print(f"Processed and saved chunk starting at row {start}")

    print("Translation completed and all data saved to 'translated_data.csv'")

# Load your data
df = pd.read_csv('suomi24/Data/filtered/s24_2001.csv')

# Specify columns to translate
columns_to_translate = ['title', 'topic_name_top', 'thread_text']

# Translate the DataFrame in chunks
translate_dataframe_in_chunks(df, columns_to_translate)
