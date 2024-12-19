import unittest

from main import read_input, search


class TestTest(unittest.TestCase):

    def test_dfs(self):
        data = read_input("./test.txt")
        self.assertEqual(search(data[0]), 280)
        self.assertEqual(search(data[2]), 200)


if __name__ == "__main__":
    unittest.main()
