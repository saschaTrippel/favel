import unittest
from ContainerService.Containers import Containers
import os
import time

pid = os.fork()


class TestContainers(unittest.TestCase):
    def setUp(self):
        self.containers = Containers()

    def testStartContainers(self):
        if pid:
            self.containers.startContainers()
            containers = self.containers.docker.compose.ps()
            self.assertGreaterEqual(len(containers), 1)
        else:
            pass


    def testStopContainers(self):
        self.containers.stopContainers()
        containers = self.containers.docker.compose.ps()
        self.assertEqual(len(containers), 0)

    def testStatusContainers(self):
        pass

    def testRemoveContainers(self):
        self.containers.rmContainers()
        containers = self.containers.docker.compose.ps()
        self.assertEqual(len(containers), 0)
