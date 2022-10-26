import unittest
from datastructures.Assertion import Assertion


class TestDataStructure(unittest.TestCase):

    def setUp(self):
        self.assertion = Assertion("Barack Obama", "born", "America")

    def testExpectedScore(self):
        self.assertion.expectedScore(1)
        self.asset

    def testGetTurtle(self):
        method = self.ctrl.getMethod()
        self.assertIn(method, ["train", "cache", "test"])

    def testCastingToString(self):
        self.ctrl.input()
        self.assertGreaterEqual(len(self.ctrl.trainingData), 1)
        self.assertGreaterEqual(len(self.ctrl.testingData), 1)
