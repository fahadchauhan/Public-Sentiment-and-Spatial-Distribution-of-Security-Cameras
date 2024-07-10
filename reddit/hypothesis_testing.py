import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from mlxtend.frequent_patterns import fpgrowth, association_rules

# Load the dataset
file_path = "C:/Users/user/OneDrive - Oulun yliopisto/Documents/suomi24/Data/suomi24.csv"
df = pd.read_csv(file_path, usecols=['thread_text_processed'])
# print(df)
print("Vectorize the text")
# Vectorize the text
vectorizer = CountVectorizer(max_df=0.90, min_df=0.01, stop_words='english', binary=True)
X = vectorizer.fit_transform(df['thread_text_processed'])
feature_names = vectorizer.get_feature_names_out()

print("Convert to DataFrame for FP-Growth")
# Convert to DataFrame for FP-Growth
df_binary = pd.DataFrame.sparse.from_spmatrix(X, columns=feature_names)

print("Apply FP-Growth")
# Apply FP-Growth
frequent_itemsets = fpgrowth(df_binary, min_support=0.01, use_colnames=True)

print("association_rules")
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

print("Define the hypotheses with synonyms included")
# Define the hypotheses with synonyms included
hypotheses = {
    'H0': {'antecedent': [['public', 'camera'], ['public', 'cctv']], 'consequent': ['privacy']},
    'H1': {'antecedent': [['surveillance', 'camera'], ['monitoring', 'cctv']], 'consequent': ['reduce', 'crime']},
    'H2': {'antecedent': [['personal', 'experience'], ['individual', 'encounter']], 'consequent': ['public', 'monitoring']},
    'H3': {'antecedent': [['trust', 'organizations'], ['confidence', 'agencies']], 'consequent': ['transparency', 'accountability']},
    'H4': {'antecedent': [['attitudes', 'camera'], ['views', 'cctv']], 'consequent': ['various', 'settings']},
    'H5': {'antecedent': [['technical', 'complaints'], ['mechanical', 'issues']], 'consequent': ['enhancements']},
    'H6': {'antecedent': [['surveillance', 'camera'], ['security', 'cctv']], 'consequent': ['secure', 'watched']},
    'H7': {'antecedent': [['density', 'camera'], ['concentration', 'cctv']], 'consequent': ['public', 'opinion']}
}

print("Test the hypotheses with synonyms")
# Test the hypotheses with synonyms
def test_hypothesis(rules, hypothesis):
    supported = False
    for index, rule in rules.iterrows():
        for antecedent in hypothesis['antecedent']:
            if set(antecedent).issubset(rule['antecedents']) and set(hypothesis['consequent']).issubset(rule['consequents']):
                supported = True
                print(f"Hypothesis supported: {antecedent} -> {hypothesis['consequent']}")
    if not supported:
        print(f"Hypothesis not supported: {hypothesis['antecedent']} -> {hypothesis['consequent']}")

print("Evaluate all hypotheses")
# Evaluate all hypotheses
for name, hypothesis in hypotheses.items():
    test_hypothesis(rules, hypothesis)
