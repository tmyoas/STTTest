import unittest
import sys
import os

abs_dirpath = os.path.abspath(os.path.dirname(__file__))

def suite():
    test_suite = unittest.TestSuite()
    suites = unittest.defaultTestLoader.discover(abs_dirpath, pattern='Test*.py')
    for test in suites:
        test_suite.addTest(test)
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())