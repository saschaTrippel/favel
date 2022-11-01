import unittest
from OutputService.Output import Output
from OutputService.Output import GerbilFormat
from datastructures.Assertion import Assertion

import pandas as pd
import os


class TestOutputService(unittest.TestCase):

    def setUp(self):
        experiment = "./../Evaluation/example/"
        self.output = Output(experiment)
        self.gerbil = GerbilFormat(self.mockTestingData(), experiment)

    def testWriteOutput(self):
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data=d)
        self.output.writeOutput(df)
        self.assertTrue(os.path.exists("./../Evaluation/example/Output.csv"))
        os.remove("./../Evaluation/example/Output.csv")

    def mockTestingData(self):
        a = Assertion("Barack Obama", "born", "America")
        a._expectedScore = 1
        return [a]

    def testCreateTripleSubject(self):
        result = self.gerbil.createTripleSubject("<http://favel/>", "born")
        self.assertEqual(result, "<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <born>.\n")

    def testCreateTripleObject(self):
        result = self.gerbil.createTripleObject("<http://favel/>", "born")
        self.assertEqual(result, "<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <born>.\n")

    def testCreateTriplePredicate(self):
        result = self.gerbil.createTriplePredicate("<http://favel/>", "born")
        self.assertEqual(result, "<http://favel/> <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <born>.\n")

    def testCreateTripleType(self):
        result = self.gerbil.createTruthValueTriple("<http://favel/>", 1.0)
        self.assertEqual(result, '<http://favel/> <http://swc2017.aksw.org/hasTruthValue> "1.0"^^<http://www.w3.org/2001/XMLSchema#double> .\n')
