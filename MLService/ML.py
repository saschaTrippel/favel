import logging
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import pickle,os
class ML:
    
#To-Do add prediction script with subject, object, predicate encoding

    def getEnsembleScore(self, df):
        result = []
        with open('MLService/models/GradientBoosting_model.pkl','rb') as f:
            model = pickle.load(f)
        result = model.predict(df)
        return result