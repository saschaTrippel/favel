import unittest
from ContainerService.Containers import Containers

class TestContainers(unittest.TestCase):

    def __init__(self):
        self.containers = Containers()


    def test_start_containers(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
    