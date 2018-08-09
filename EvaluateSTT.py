import argparse
import io
import sys
import numpy

class Levenshtein_distance():
    insertion_error = []
    deletion_error = []
    substitution_error = []
    num_all_words = 0

    def __init__(self, trans, ans):
        self.trans = trans
        self.ans = ans
        self.num_all_words = len(self.ans)

    def get_e_ins(self):
        return self.insertion_error[-1][-1]

    def get_e_del(self):
        return self.deletion_error[-1][-1]

    def get_e_sub(self):
        return self.substitution_error[-1][-1]

    def get_num_all(self):
        return self.num_all_words

    def evaluateSTT(self):
        m = numpy.zeros((len(self.ans) + 1) * (len(self.trans) + 1), dtype = numpy.uint16)
        m = numpy.reshape(m, (len(self.ans) + 1, len(self.trans) + 1))

        self.insertion_error = numpy.zeros((len(self.ans) + 1) * (len(self.trans) + 1), dtype = numpy.uint16)
        self.insertion_error = numpy.reshape(self.insertion_error, (len(self.ans) + 1, len(self.trans) + 1))

        self.deletion_error = numpy.zeros((len(self.ans) + 1) * (len(self.trans) + 1), dtype = numpy.uint16)
        self.deletion_error = numpy.reshape(m, (len(self.ans) + 1, len(self.trans) + 1))

        self.substitution_error = numpy.zeros((len(self.ans) + 1) * (len(self.trans) + 1), dtype = numpy.uint16)
        self.substitution_error = numpy.reshape(m, (len(self.ans) + 1, len(self.trans) + 1))

        for i in range(len(self.ans) + 1):
            m[i][0] = i

        for j in range(len(self.trans) + 1):
            m[0][j] = j

        for i in range(1, len(self.ans) + 1):
            for j in range(1, len(self.trans) + 1):
                if self.ans[i - 1] == self.trans[j - 1]:
                    m[i][j] =m[i - 1][j - 1]
                else:
                    # distance_list = [ins_distance, del_distance, sub_distance]
                    distance_list = [m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + 1]
                    m[i][j] = min(distance_list)
                    if numpy.argmin(distance_list) == 0:
                        self.insertion_error[i][j] = self.insertion_error[i - 1][j] + 1
                    elif numpy.argmin(distance_list) == 1:
                        self.deletion_error[i][j] = self.deletion_error[i][j - 1] + 1
                    else:
                        self.substitution_error[i][j] = self.substitution_error[i - 1][j - 1] + 1
        print(m[-1][-1])
        return m[-1][-1] / self.get_num_all()

if __name__ == '__main__':
    # Setting of command-line parameters
    # transcription: result of Speech to Text
    # answer: correct words
    parser = argparse.ArgumentParser()
    parser.add_argument('transcription', help='A file of result Speech to Text.')
    parser.add_argument('answer', help='A file of correct answer data.')

    fin = open(parser.parse_args().transcription)
    transcription_list = fin.read().split(" ")
    fin = open(parser.parse_args().answer)
    answer_list = fin.read().split(" ")
    fin.close()

    # print(transcription_list[0])
    # print(answer_list[0])

    evaluate = Levenshtein_distance(transcription_list, answer_list)
    print('WER: %f' % evaluate.evaluateSTT())
    print('ins: %d, del: %d, sub: %d, words: %d' % (evaluate.get_e_ins(), evaluate.get_e_del(), evaluate.get_e_sub(), evaluate.get_num_all()))

