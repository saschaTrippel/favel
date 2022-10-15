import logging
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import pickle,os
import numpy as np

class ML:

    def __init__(self):
        with open('MLService/models/classifier.pkl','rb') as fp: 
            self.model=pickle.load(fp)
        with open('MLService/models/le_predicate.obj','rb') as fp: 
            self.le_predicate=pickle.load(fp)

    def createDataFrame(self,assertionScores,approaches):
        """
        To create the DataFrame that consists of triples and scores from each approach for that particular triple.
        """
        result = dict()
        result['subject'] = []
        result['predicate'] = []
        result['object'] = []

        for assertionScore in assertionScores:
            result['subject'].append(assertionScore.subject)
            result['predicate'].append(assertionScore.predicate)
            result['object'].append(assertionScore.object)

            for approach in approaches.keys():
                try:
                    if str(approach) in result:
                        result[str(approach)].append(assertionScore.score[str(approach)])
                    else:
                        result[str(approach)] = [assertionScore.score[str(approach)]]
                except KeyError as ex:
                    pass

        df = pd.DataFrame(result)
        
        return(df)

    def getEnsembleScore(self, assertionScores,approaches):
        pass