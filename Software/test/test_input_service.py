import unittest
from InputService.Input import Input
from InputService.ReadFiles import ReadFiles
from datastructures.Assertion import Assertion
import pandas as pd


class TestInputService(unittest.TestCase):

    def setUp(self):
        self.path = "./../Favel_Dataset/"
        self.input = Input()
        self.readFile = ReadFiles()

    def testGetInput(self):
        train, test = self.input.getInput(self.path)
        self.assertIsInstance(train[0], Assertion)
        self.assertIsInstance(test[0], Assertion)
        self.assertGreater(len(train), 1)
        self.assertGreater(len(test), 1)

    def createMockForTriples(self):
        d = {'subject': ["<http://favel/Donald>", "<http://favel/Donald>"],
             'predicate': ["<http://favel/born>", "<http://favel/born>"],
             'object': ["<http://favel/Africa>", "<http://favel/America>"], 'ensemble_score': [0, 1]}
        return pd.DataFrame(data=d)

    def testParseTriples(self):
        result = self.input.parseTriples(self.createMockForTriples())
        self.assertIsInstance(result[0], Assertion)
        self.assertEqual(result[0].expectedScore, 0)
        self.assertGreater(len(result), 1)

    def testExtractFavelTriples(self):
        triple = self.readFile.extract_favel_triples(self.path+"Turtle/Test/Correct/Movie-Director/movie-director-0.ttl")
        self.assertEqual(triple[0], "http://dbpedia.org/resource/Legend_(2014_film)")
        self.assertEqual(triple[1], "http://dbpedia.org/property/director")
        self.assertEqual(triple[2], "http://dbpedia.org/resource/Boyapati_Srinu")

    def testGetFavel(self):
        train, test = self.readFile.getFavel(self.path)
        self.assertIsInstance(train, pd.DataFrame)
        self.assertGreater(len(train), 1)
        self.assertGreater(len(test), 1)
