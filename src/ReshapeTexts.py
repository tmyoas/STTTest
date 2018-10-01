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
        temp_list.append(re.sub(del_pattern, ins_pattern, input_list[i]))
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def remove_additional_info(input_list):
    # remove "Transcript:[ ]*", "Confidence: [0-9.]\n" for STTfromGS.py
    pattern = r'transcript:[ ]*|confidence: [0-9.]\n|[0-9]{2}:[0-9]{2}:[0-5][0-9].?'
    return replace_patterns(pattern, '', input_list)

def remove_line_feed_code(input_list):
    # DONE remove "\r" and "\n"
    temp_list = []
    for i in range(0, len(input_list) - 1):
        temp_list.append(input_list[i].strip())
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def remove_space_around_apostrophe(input_list):
    # remove <sp> around "'"
    del_pattern = r" '|' "
    ins_pattern = r"'"
    return replace_patterns(del_pattern, ins_pattern, input_list)

def replace_space(input_list):
    # replace [ ]+ to " "
    del_pattern = r'[ ]+'
    ins_pattern = ' '
    return replace_patterns(del_pattern, ins_pattern, input_list)

def remove_punctuation(input_list):
    # DONE also remove ",", ".", "!", and "?"
    pattern = r"[,.!?]+."
    return replace_patterns(pattern, '', input_list)

def get_reshaped_texts(input_list):
    # TODO:
    # how to change "-"

    # unify upper / lower case.
    for i in range(0, len(input_list) - 1):
        input_list[i] = input_list[i].lower()

    ans_list = remove_additional_info(input_list)
    ans_list = remove_line_feed_code(ans_list)
    ans_list = remove_space_around_apostrophe(ans_list)
    ans_list = replace_space(ans_list)
    ans_list = remove_punctuation(ans_list)
    return ' '.join(ans_list)

def make_output_file(parser):
    return 0


if __name__ == '__main__':
    # Setting of command-line parameters
    # target: A file that you want to reshape
    # file: output filepath and filename
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='A reshape-target file.')
    parser.add_argument('output', nargs='?', help='An output file (default: <target filename>_reshaped.txt)')

    fin = open(parser.parse_args().target, encoding="utf8")
    input_list = fin.readlines()
    fin.close()

    # reshape_texts
    output = get_reshaped_texts(input_list)

    # TODO: separate method (make_output_file)
    if not parser.parse_args().output:
        targetpath = os.path.split(parser.parse_args().target)
        outputpath = (targetpath[0], targetpath[1].replace('.', '_reshaped.'))
    else:
        outputpath= os.path.split(parser.parse_args().output)
    os.makedirs(outputpath[0], exist_ok=True)
    fout = open(os.path.join(outputpath[0], outputpath[1]), mode='w', encoding="utf8")
    fout.write(output)
    fout.close()


