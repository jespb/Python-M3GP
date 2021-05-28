import pandas

from m3gp.M3GP import M3GP

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

import warnings

warnings.filterwarnings("ignore", category=FutureWarning,
                        message="From version 0.21, test_size will always complement",
                        module="sklearn")

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
#



filename= "heart.csv"

# Open the dataset
ds = pandas.read_csv("datasets/"+filename)
class_header = ds.columns[-1]

# Split the dataset
Tr_X, Te_X, Tr_Y, Te_Y = train_test_split(ds.drop(columns=[class_header]), ds[class_header], 
		train_size=0.7, random_state = 42, stratify = ds[class_header])

# Train a model
m3gp = M3GP()
m3gp.fit(Tr_X, Tr_Y)

# Predict test results
pred = m3gp.predict(Te_X)

# Obtain test accuracy
print( accuracy_score(pred, Te_Y) )

