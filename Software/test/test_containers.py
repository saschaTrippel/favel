import unittest
from ContainerService.Containers import Containers


class TestContainers(unittest.TestCase):
    def setUp(self):
        self.containers = Containers()

    def testStartContainers(self):
        self.containers.startContainers()
        print(self.containers.docker.compose.images())

