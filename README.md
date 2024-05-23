downloaded reddit data from: https://the-eye.eu/redarcs/ I converted Reddit zst files to csv using a repo: https://github.com/ArthurHeitmann/arctic_shift the filtered csv to have data from the relevant keywords using: filter_csv.py

downloaded suomi24 data from: https://korp.csc.fi/download/Suomi24/ converted data from zip to csv using: zip_to_csv.py

then filtered data using filter_suomi24_csv.py by phrases mentioned in the py file

then tried to translate the data using google_translate website through selenium but google doesn't let the selenium tanslate docs

then i used the model opus model given by helsinki university to translate finnish data to english

then i cleaned data and then combined the 20 csvs of 20 years of data into 1 csv file
in cleaning i converted some utf-8 encoded characters like 'â€™ to appostrofe(') and kept only ascii characters. and removed duplicated sentences to remove noise and spam.

first i did proprocessing: lower case, remove numbers, remove multiple spaces, remove punctuations, remove single and double characters to dodge utf-8 encoding characrets like '&gt' and removed stopwords and applied word lemmatization and saved the text into a new column named processed_text

then i did some analysis in Trends.ipynb notebook, where i displayed;
Monthly Trends in Discussions Over Time
WordCloud
Heatmap of Discussions Over Time
Keyword Frequencies of the keywords mentioned in the notebook cell
Co-occurrence Heatmap of the same Keywords

then i did LDA topic modelling in LDA_Topic_Modelling.ipynb notebook,
converted sentences to words
applied bigrams and trigrams
lemmatize the text and kept only allowed_postags=['NOUN','ADJ','VERB','ADV']
created id2word dictionary
created a corpus of the words
trained an genism LDAmodel
did hyperparameter tuning and num_topics=3 and passes=20 were the tuned paramter values
check lda performance through coherence score
displayed the pyLDAvis visualization to see top-30 most salient terms in 3 topics

then i tried the bert topic modelling
bertModel was taking a lot of time so used an embedding_model="distilbert-base-nli-mean-tokens"


