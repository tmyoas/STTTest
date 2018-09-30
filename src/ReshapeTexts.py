import argparse
import io
import sys
import numpy
import re
import os
import datetime
import re

def remove_additional_info(input_list):
    pattern = r'Transcript:[ ]*|Confidence: [0-9.]\n|[0-9]{2}:[0-9]{2}:[0-5][0-9]'
    input_list = [i.replace(pattern, '') for i in input_list]
    while '' in input_list:
        input_list.remove('')
    return input_list

def remove_line_feed_code():
    return 0

def replace_delimiter():
    return 0

def remove_space_around_apostrophe():
    return 0

def remove_punctuation():
    return 0

def get_reshaped_texts(self):
    # TODO:
    # remove "Transcript:[ ]*", "Confidence: [0-9.]\n" for STTfromGS.py
    # remove "\r" and "\n". : rstrip?
    # replace "-" to " "
    # replace [ ]+ to " " : split(" ") -> if list[n] == "" : del list[n] ?
    # remove <sp> around "'". : [ ]*'[ ]* -> '
    # also remove ",", ".", "!", and "?"
    # NO NEED to unify upper / lower case.
    return 0

def make_output_file(parser):
    return 0


if __name__ == '__main__':
    # Setting of command-line parameters
    # target: A file that you want to reshape
    # file: output filepath and filename
    parser = argparse.ArgumentParser()
    parser.add_argument('target', nargs='1', help='A reshape-target file.')
    parser.add_argument('output', nargs='?', help='An output file (default: <target filename>_reshaped.txt)')

    fin = open(parser.parse_args().target, encoding="utf8")
    input_list = fin.readlines()
    fin.close()

    # reshape_texts

    # TODO: separate method (make_output_file)
    if not parser.parse_args().output:
        targetpath = os.path.split(parser.parse_args().target)
        outputpath = (targetpath[0], targetpath[1].replace('.', '_reshaped.'))
    else:
        outputpath= os.path.split(parser.parse_args().output)
    os.makedirs(outputpath[0], exist_ok=True)
    file = open(parser.parse_args().output, mode='w', encoding="utf8")
    # TODO: output in file
    file.close()


