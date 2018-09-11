import unittest
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
from src.EvaluateSTT import Levenshtein_distance

class Test_Levenshtein_distance(unittest.TestCase):

    def test_calcWER_correct(self):
        transcription_list = ['This', 'is', 'a', 'pen']
        answer_list = ['This', 'is', 'a', 'pen']
        expected_num_all = 4
        expected_ins = 0
        expected_sub = 0
        expected_del = 0
        expected_wer = (expected_ins + expected_sub + expected_del) / expected_num_all
        actual = Levenshtein_distance(transcription_list, answer_list)

        self.assertEqual(actual.get_num_all(), expected_num_all)
        self.assertEqual(actual.get_WER(), expected_wer)
        self.assertEqual(actual.get_error_type()['ins'], expected_ins)
        self.assertEqual(actual.get_error_type()['sub'], expected_sub)
        self.assertEqual(actual.get_error_type()['del'], expected_del)

    def test_calcWER_ins(self):
        transcription_list = ['This', 'is', 'a', 'pen', 'and', 'notebook']
        answer_list = ['This', 'is', 'a', 'pen']
        expected_num_all = 4
        expected_ins = 2
        expected_sub = 0
        expected_del = 0
        expected_wer = (expected_ins + expected_sub + expected_del) / expected_num_all
        actual = Levenshtein_distance(transcription_list, answer_list)

        self.assertEqual(actual.get_num_all(), expected_num_all)
        self.assertEqual(actual.get_WER(), expected_wer)
        self.assertEqual(actual.get_error_type()['ins'], expected_ins)
        self.assertEqual(actual.get_error_type()['sub'], expected_sub)
        self.assertEqual(actual.get_error_type()['del'], expected_del)

    def test_calcWER_sub(self):
        transcription_list = ['This', 'is', 'a', 'notebook']
        answer_list = ['This', 'is', 'a', 'pen']
        expected_num_all = 4
        expected_ins = 0
        expected_sub = 1
        expected_del = 0
        expected_wer = (expected_ins + expected_sub + expected_del) / expected_num_all
        actual = Levenshtein_distance(transcription_list, answer_list)

        self.assertEqual(actual.get_num_all(), expected_num_all)
        self.assertEqual(actual.get_WER(), expected_wer)
        self.assertEqual(actual.get_error_type()['ins'], expected_ins)
        self.assertEqual(actual.get_error_type()['sub'], expected_sub)
        self.assertEqual(actual.get_error_type()['del'], expected_del)

    def test_calcWER_del(self):
        transcription_list = ['This', 'is', 'pen']
        answer_list = ['This', 'is', 'a', 'pen']
        expected_num_all = 4
        expected_ins = 0
        expected_sub = 0
        expected_del = 1
        expected_wer = (expected_ins + expected_sub + expected_del) / expected_num_all
        actual = Levenshtein_distance(transcription_list, answer_list)

        self.assertEqual(actual.get_num_all(), expected_num_all)
        self.assertEqual(actual.get_WER(), expected_wer)
        self.assertEqual(actual.get_error_type()['ins'], expected_ins)
        self.assertEqual(actual.get_error_type()['sub'], expected_sub)
        self.assertEqual(actual.get_error_type()['del'], expected_del)

    def test_calcWER_complicate(self):
        transcription_list = ['All', 'you', 'need', 'is', 'kill']
        answer_list = ['This', 'is', 'a', 'pen']
        expected_num_all = 4
        expected_total = 5
        expected_wer = expected_total / expected_num_all
        actual = Levenshtein_distance(transcription_list, answer_list)

        self.assertEqual(actual.get_num_all(), expected_num_all)
        self.assertEqual(actual.get_WER(), expected_wer)
        self.assertEqual(actual.get_error_type()['ins'] + actual.get_error_type()['sub'] + actual.get_error_type()['del'], expected_total)

if __name__ == "__main__":
    unittest.main()