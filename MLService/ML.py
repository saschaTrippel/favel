import logging
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import pickle,os

class ML:

    def __init__(self):
        with open('MLService/models/classifier.pkl','rb') as fp: 
            self.model=pickle.load(fp)
        
    def getEnsembleScore(self, input_df):
        # input_df=pd.DataFrame.from_dict([input_dict])
        pred = []
        input_df=input_df.drop(['subject','object','predicate'], axis=1)
        pred=self.model.predict(input_df)
        return pred