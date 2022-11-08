import unittest

from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
import numpy as np
from MLService.ML import ML
import pandas as pd
from datastructures.Assertion import Assertion


def createMockForTriples():
    approaches = {"Adamic_Adar": 4000, "Copaal": 3333}
    data = []
    for i in range(3):
        assertion = Assertion("<http://favel/Donald>", "<http://favel/born>", "<http://favel/Africa" + str(i) + ">")
        assertion.expectedScore = i % 2
        data.append(assertion)
    return data, approaches


class TestMLService(unittest.TestCase):

    def setUp(self):
        self.path = "./../Favel_Dataset/"
        self.ml = ML(self.path + "log.txt")

    def getFakeDataForML(self):
        data, approaches = createMockForTriples()
        return self.ml.createDataFrame(data, approaches)

    def testCreateDataFrame(self):
        self.assertIsInstance(self.getFakeDataForML(), pd.DataFrame)

    def testTrainModel(self):
        data = self.getFakeDataForML()
        data["truth"] = [0, 1, 0]
        a = self.ml.train_model(data,
                                DecisionTreeClassifier(),
                                self.path, self.path)
        self.assertEqual(a, True)

    def testGetModelName(self):
        self.assertEqual(self.ml.get_model_name(DecisionTreeClassifier()), "DecisionTreeClassifier")

    def testCustomModelTrainCv(self):
        df = self.getFakeDataForML()
        df["truth"] = [0, 1, 0]
        le = preprocessing.LabelEncoder()
        le.fit(df['predicate'])
        df['predicate'] = le.transform(np.array(df['predicate'].astype(str), dtype=object))

        X = df.drop(['truth', 'subject', 'object'], axis=1)
        y = df.truth
        a = self.ml.custom_model_train_cv(X, y, DecisionTreeClassifier())
        print(a)