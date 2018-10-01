import argparse
import io
import sys
import numpy
import re
import os
import datetime
import re

def replace_patterns(del_pattern, ins_pattern, input_list):
    temp_list = []
    for i in range(0, len(input_list) - 1):
        temp_list[i] = re.sub(del_pattern, ins_pattern, input_list[i])
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def remove_additional_info(input_list):
    pattern = r'transcript:[ ]*|confidence: [0-9.]\n|[0-9]{2}:[0-9]{2}:[0-5][0-9].?'
    return replace_patterns(pattern, '', input_list)

def remove_line_feed_code(input_list):
    temp_list = []
    for i in range(0, len(input_list) - 1):
        temp_list[i] = input_list[i].strip()
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def remove_space_around_apostrophe(input_list):
    del_pattern = r" '|' "
    ins_pattern = r"'"
    replace_patterns(del_pattern, ins_pattern, input_list)
    return input_list

def replace_delimiter(input_list):
    return input_list

def remove_punctuation():
    return input_list

def get_reshaped_texts(input_list):
    # TODO:
    # DONE unify upper / lower case.
    # DONE remove "Transcript:[ ]*", "Confidence: [0-9.]\n" for STTfromGS.py
    # DONE remove "\r" and "\n". : strip?
    # DONE remove <sp> around "'". : [ ]*'[ ]* -> '
    # replace "-" -> split("-")
    # replace [ ]+ to " " : split(" ") -> if list[n] == "" : del list[n] ?
    # also remove ",", ".", "!", and "?"

    for i in range(0, len(input_list) - 1):
        input_list[i] = input_list.lower()

    list = []

    return ' '.join(list)

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


