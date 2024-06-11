downloaded Reddit data from: https://the-eye.eu/redarcs/ I converted Reddit ZST files to CSV using a repo: https://github.com/ArthurHeitmann/arctic_shift the filtered CSV to have data from the relevant keywords using: filter_csv.py

downloaded suomi24 data from: https://korp.csc.fi/download/Suomi24/ converted data from zip to CSV using: zip_to_csv.py

then filtered data using filter_suomi24_csv.py by phrases mentioned in the py file

then tried to translate the data using the google_translate website through Selenium but Google doesn't let the Selenium translate docs

then I used the model opus model given by Helsinki University to translate Finnish data into English

then I cleaned data and then combined the 20 csvs of 20 years of data into 1 csv file
in cleaning I converted some UTF-8 encoded characters like 'â€™ to apostrophe (') and kept only ASCII characters. and removed duplicated sentences to remove noise and spam.

first, I did preprocessing: lowercase, removed numbers, removed multiple spaces, punctuations, single and double characters to dodge utf-8 encoding characters like '&gt' removed stopwords applied word lemmatization saved the text into a new column named processed_text

then I did some analysis in Trends.ipynb notebook, where I displayed;
Monthly Trends in Discussions Over Time
WordCloud
Heatmap of Discussions Over Time
Keyword Frequencies of the keywords mentioned in the notebook cell
Co-occurrence Heatmap of the same Keywords

then I did LDA topic modelling in LDA_Topic_Modelling.ipynb notebook,
converted sentences to words
applied bigrams and trigrams
lemmatize the text and keep only allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']
created id2word dictionary
created a corpus of the words
trained an genism LDAmodel
did hyperparameter tuning and num_topics=3 and passes=20 were the tuned parameter values
Check LDA performance through coherence score
displayed the pyLDAvis visualization to see top-30 most salient terms in 3 topics

then I tried the Bert topic modelling
bertModel was taking a lot of time so used an embedding_model="distilbert-base-nli-mean-tokens"
it generated a lot of topics so I fine-tuned the number of topic parameters using the coherence score as a metric.
used the reduce_topics function by Bertopic and then the reduce_outliers function by Bertopic to reduce outliers.
merged some topics which had less data with the bigger topics.
in the end, we had 3 topics but still, 1 topic has multiple aspects like privacy and security and opinions of personal experiences in all together.
tried to further split into sub-topics but no approach worked, I tried k-means, LDA and Bertopic on that topic data but nothing worked.

Then we created a hypothesis and created embedding of the rows and the hypothesis,
used cosine similarity to assign rows to the hypothesis so that these hypotheses can be used as aspects.

Tried the BerTweet for sentiment after this, but all of the rows turned into negative sentiment.


