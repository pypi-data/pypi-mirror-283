import pandas as pd
import string

from optialgo.text_preprocessing import  *


import time


def get_data(lang='indonesian',size:int=None):
    if lang == "indonesian":
        df = pd.read_csv('review-pln-mobile.csv')['ulasan']
    else:
        df = pd.read_csv("../dataset_ex/IMDB.csv")['review']
    if size:
        return df.iloc[:size]
    return df



lang = "indonesian"
data = get_data(lang=lang).tolist()
t = text_clean(data,return_token=True)
start = time.time()

stopwords = get_stopwords_idn()

stopwords.extend(['nya','yg'])

tm = text_manipulation(t,lang=lang,return_token=False,verbose=True,return_dataframe=False,stem=False,stopwords=True)
end = time.time()

time_ = end - start

print(f"{time_:.6f}")

tokenizer = Tokenizer(data=tm)

print(tokenizer.word_index)


# english
# 3 seconds : stem (return_token=False)
# 655.75 seconds : lemma

# Indonesian
# 0.71 seconds : lemma
# 175 seconds (stem caching (return_token=False))
# 1016.308040 (stem manual)







