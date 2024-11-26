import pandas as pd
import numpy as np
import math
from collections import defaultdict, Counter
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Load your dataset
df = pd.read_csv('/Users/arianeglon/Desktop/Final_Project_COMP370/Annotations_clean.csv', sep=';')

print(df.columns)

# Load stop words from your file
with open('./stop_words', 'r') as f:
    stop_words = set(f.read().splitlines())

def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-z]+\b', text)
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

all_texts = (df['Article Name'] + ' ' + df['Description']).fillna('')
all_docs_tokens = [preprocess(text) for text in all_texts]
df_counts = defaultdict(int)
N = len(all_docs_tokens)

for tokens in all_docs_tokens:
    unique_tokens = set(tokens)
    for token in unique_tokens:
        df_counts[token] += 1

#IDF computations here
idf = {}
for word, df_count in df_counts.items():
    idf[word] = math.log(N / (df_count + 1))

annotated_df = df.dropna(subset=['Tag '])
categories = annotated_df['Tag '].unique()

category_texts = {}
for category in categories:
    category_df = annotated_df[annotated_df['Tag '] == category]
    texts = (category_df['Article Name'] + ' ' + category_df['Description']).fillna('')
    category_texts[category] = texts.tolist()

category_tf = {}
for category, texts in category_texts.items():
    tf_counts = Counter()
    for text in texts:
        tokens = preprocess(text)
        tf_counts.update(tokens)
    category_tf[category] = tf_counts

category_tfidf = {}
for category, tf_counts in category_tf.items():
    tfidf_scores = {}
    for word, tf in tf_counts.items():
        if word in idf:
            tfidf_scores[word] = tf * idf[word]
    category_tfidf[category] = tfidf_scores

for category, tfidf_scores in category_tfidf.items():

    sorted_words = sorted(tfidf_scores.items(), key=lambda item: item[1], reverse=True)
    top_10_words = sorted_words[:10]

for category, tfidf_scores in category_tfidf.items():
    sorted_words = sorted(tfidf_scores.items(), key=lambda item: item[1], reverse=True)
    top_10_words = sorted_words[:10]
    
    print(f"Top 10 words for category '{category}':")
    for word, score in top_10_words:
        print(f"{word}: {score:.4f}")
    print()