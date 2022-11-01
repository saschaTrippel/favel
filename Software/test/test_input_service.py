import unittest
from InputService.Input import Input
from datastructures.Assertion import Assertion
import pandas as pd


class TestInputService(unittest.TestCase):

    def setUp(self):
        self.path = "./../Favel_Dataset/"
        self.input = Input()

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
        self.input.parseTriples(self.createMockForTriples())
