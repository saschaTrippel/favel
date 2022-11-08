import unittest
from MLService.ML import ML
import pandas as pd
from datastructures.Assertion import Assertion


def createMockForTriples():

    approaches = {"Adamic_Adar": 4000, "Copaal": 3333}
    data = []
    for i in range(3):
        assertion = Assertion("<http://favel/Donald>", "<http://favel/born>", "<http://favel/Africa"+str(i)+">")
        assertion.expectedScore = i % 2
        data.append(assertion)
    return data, approaches


class TestMLService(unittest.TestCase):

    def setUp(self):
        self.path = "./../Favel_Dataset/"
        self.ml = ML(self.path + "log.txt")

    def testCreateDataFrame(self):
        data, approaches = createMockForTriples()
        test = self.ml.createDataFrame(data, approaches)
        self.assertIsInstance(test, pd.DataFrame)

