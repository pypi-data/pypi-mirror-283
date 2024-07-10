import pandas as pd
import numpy as np
import sys
path = "/home/lopyu/myrepo/opensource/optialgo"
sys.path.append(path)
from optialgo import Dataset,TextDataset,text_clean,text_manipulation,Tokenizer
from optialgo import Classification
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer


# TODO: DONE
df = pd.read_csv("tests/review-pln-mobile.csv")


feature = "ulasan"
target = "rating"

dataset = TextDataset(df)
vect = TfidfVectorizer(max_features=500)

dataset.fit(feature=feature,target=target,lang="indonesian",t="classification",vectorizer='tfidf',verbose=False)

clf = Classification(dataset=dataset,algorithm='Naive Bayes')

text = "Udah pengajuan menambah speed iconnet dari 10mbps ke 20mbps, katanya nnti akan di infokan melalui apa gtu gmail atau pesan, sampe sekarang belum ada info apa2"
arr = [
    text,
    "aku dimana"
]