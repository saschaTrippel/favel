import logging
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import pickle,os
import numpy as np
from OutputService.Output import Output

class ML:

    def __init__(self):
        with open('MLService/models/classifier.pkl','rb') as fp: 
            self.model=pickle.load(fp)
        with open('MLService/models/le_predicate.obj','rb') as fp: 
            self.le_predicate=pickle.load(fp)

    def getEnsembleScore(self, assertionScores,approaches):

        # TODO: must not make a call to OutputService, otherwise services would be coupled
        op = Output()
        input_df = op.getOutput(assertionScores,approaches)

        ensembleScore = []
        input_df['predicate'] = input_df['predicate'].map(lambda s: '<unknown>' if s not in self.le_predicate.classes_ else s)
        self.le_predicate.classes_ = np.append(self.le_predicate.classes_, '<unknown>')
        input_df.predicate = self.le_predicate.transform(input_df.predicate)
        input_df = input_df.drop(['subject','object'], axis=1)
        ensembleScore = self.model.predict(input_df)
        
        input_df['ensemble_score'] = ensembleScore

        return(input_df)