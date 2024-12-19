import unittest

from main import search, read_input


class TestTest(unittest.TestCase):

    def test_dfs(self):
        data = read_input("./test.txt")
        self.assertEqual(search(data[0], (0, 0)), 280)
        self.assertEqual(search(data[2], (0, 0)), 200)


if __name__ == "__main__":
    unittest.main()
