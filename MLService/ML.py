import logging
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import pickle,os



class ML:

    def __init__(self):
        with open('MLService/models/GradientBoosting_model.pkl','rb') as fp: 
            self.model=pickle.load(fp)

        with open('MLService/models/le_subject.pkl','rb') as fp: 
            self.le_subject=pickle.load(fp)

        with open('MLService/models/le_predicate.pkl','rb') as fp: 
            self.le_predicate=pickle.load(fp)

        with open('MLService/models/le_object.pkl','rb') as fp: 
            self.le_object=pickle.load(fp)

        
        
    def getEnsembleScore(self, input_df):
        # input_df=pd.DataFrame.from_dict([input_dict])
        
        input_df.subject  = self.le_subject.transform(input_df.subject)
        input_df.predicate= self.le_predicate.transform(input_df.predicate)
        input_df.object   = self.le_object.transform(input_df.object)

        pred=self.model.predict_proba(input_df)[0]
        
        return pred
