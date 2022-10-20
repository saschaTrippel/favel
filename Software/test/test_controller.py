import unittest
from controller.Controller import Controller


class TestController(unittest.TestCase):

    def setUp(self):
        self.ctrl = Controller(["-e", "example", "-d", "./../Favel_Dataset"])

    def test_loadConfig(self):
        self.ctrl._loadConfig()
        self.assertIn("Approaches", self.ctrl.configParser)
        self.assertIn("MLApproches", self.ctrl.configParser)
        self.assertIn("General", self.ctrl.configParser)
        self.assertIn("logging", self.ctrl.configParser["General"])
        self.assertIn("cachePath", self.ctrl.configParser["General"])
        self.assertIn("useCache", self.ctrl.configParser["General"])

    def test_getMethod(self):
        method = self.ctrl.getMethod()
        self.assertIn(method, ["train", "cache", "test"])

    def test_input(self):
        self.ctrl.input()
        self.assertGreaterEqual(len(self.ctrl.trainingData), 1)
        self.assertGreaterEqual(len(self.ctrl.testingData), 1)
