import pandas as pd
import os
import sys
path = "/home/lopyu/myrepo/opensource/optialgo"
sys.path.append(path)
import numpy as np
from optialgo import Dataset,Classification


df = pd.read_csv('dataset_ex/drug200.csv')

features = df.columns.tolist()[:-1]

target = "Drug"


dataset = Dataset(dataframe=df)
dataset.fit(features=features,target=target,t='classification')

clf = Classification(dataset=dataset,algorithm="Decision Tree")

clf.predict_cli()