import unittest
import sys
import os

abs_dirpath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(abs_dirpath, '../'))
from src import STTfromGS


class Test_STTfromGS(unittest.TestCase):
    def test_get_stringlist_from_file(self):
        path = os.path.join(abs_dirpath, './resources/stringlist')
        actual = STTfromGS.get_stringlist_from_file(path)
        expected = ['test', '1', '2', '3', '4']

        self.assertEqual(actual, expected)

    def test_get_hashmap_from_file(self):
        path = os.path.join(abs_dirpath, './resources/hashmap')
        actual = STTfromGS.get_hashmap_from_file(path)
        expected = {'hoge':'fiz', 'fuga':'buzz', 'hogehoge':'fizbuzz'}

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
