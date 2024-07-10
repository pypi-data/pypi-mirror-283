import pandas as pd
from optialgo.text_preprocessing import  *


df = pd.read_csv("review-pln-mobile.csv")
ulasan = df['ulasan'].tolist()

textClean = text_clean(ulasan,verbose=True,return_token=False,return_dataframe=False)


tokenizer = Tokenizer(data=textClean,maxlen=20)
# print(count_words(textClean,min_count=700))
print(tokenizer.texts_to_pad_sequences(["aplikasi dan aku adalah"]))





