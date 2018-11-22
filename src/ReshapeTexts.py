import argparse
import os
import re
import chardet
import inflect

def replace_patterns(del_pattern, ins_pattern, input_list):
    temp_list = []
    for i in range(0, len(input_list)):
        temp_list.append(re.sub(del_pattern, ins_pattern, input_list[i]))
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def replace_multi_patterns(del_pattern_list, ins_pattern_list, input_list):
    temp_list = []
    for i in range(0, len(input_list)):
        for j in range(0, min(len(del_pattern_list), len(ins_pattern_list))):
            temp_list.append(re.sub(del_pattern_list[j], ins_pattern_list[j], input_list[i]))
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def remove_patterns(del_pattern, input_list):
    return replace_patterns(del_pattern, '', input_list)

def remove_nontarget_speaker(input_list, target):
    # remove "<Nontarget speaker name>: .*" from answer transcription
    pattern = r'^(' + target + ':).*'
    for i in range(0, len(input_list)):
        if re.match(pattern, input_list[i]):
            input_list[i + 1] = '\n'
    return input_list

def remove_speaker_name(input_list):
    # remove "<Speaker name>:[ ]*" from answer transcription
    pattern = r'\A[A-Z?][a-zA-Z?]+:'
    return remove_patterns(pattern, input_list)

def replace_equal_expressions(input_list):
    # TODO: make a method to transform equal pattern
    # def replace_equal_patterns(input_list):
        # replace 'no.' to 'number'
        # replace 'okay' to 'ok'
        # replace 'numeric' to 'alphabet words'
    del_pattern_list = []
    ins_pattern_list = []
    del_pattern_list.append(r'no.')
    ins_pattern_list.append(r'number ')
    del_pattern_list.append(r'okay')
    ins_pattern_list.append(r'ok')
    return replace_multi_patterns(del_pattern_list, ins_pattern_list, input_list)

def remove_additional_info(input_list):
    # remove "Transcript:[ ]*", "Confidence: [0-9.]\n" for STTfromGS.py
    pattern = r'transcript:[ ]*|confidence: [0-9.]*\n|[0-9]{2}:[0-9]{2}:[0-5][0-9].?'
    return remove_patterns(pattern, input_list)

def remove_line_feed_code(input_list):
    # DONE remove "\r" and "\n"
    temp_list = []
    for i in range(0, len(input_list)):
        temp_list.append(input_list[i].strip())
    while '' in temp_list:
        temp_list.remove('')
    return temp_list

def remove_space_around_apostrophe(input_list):
    # remove <sp> around "'"
    del_pattern = r" '|' |’"
    ins_pattern = r"'"
    return replace_patterns(del_pattern, ins_pattern, input_list)

def replace_metachar(input_list):
    del_pattern = '\.\.\.|\*\*\*|\-'
    ins_pattern = ' '
    return replace_patterns(del_pattern, ins_pattern, input_list)

def replace_space(input_list):
    # replace [ ]+ to " "
    del_pattern = r'[ ]+'
    ins_pattern = ' '
    return replace_patterns(del_pattern, ins_pattern, input_list)

def remove_punctuation(input_list):
    # DONE also remove ",", ".", "!", "?", and " " at the end of sentences
    pattern = r"[ ]?[,.!?]+|' '\Z"
    return remove_patterns(pattern, input_list)

def get_reshaped_texts(input_list, parser):
    # TODO:
    # how to change "-"

    # run before unifying upper / lower case for detecting speaker name.
    if parser.parse_args().name:
        ans_list = remove_nontarget_speaker(input_list, parser.parse_args().name)
    else:
        ans_list = input_list
    ans_list = remove_speaker_name(ans_list)

    # unify upper / lower case.
    for i in range(0, len(ans_list)):
        ans_list[i] = ans_list[i].lower()

    ans_list = remove_additional_info(ans_list)
    ans_list = remove_line_feed_code(ans_list)
    ans_list = remove_space_around_apostrophe(ans_list)
    ans_list = replace_metachar(ans_list)
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
    parser.add_argument('--name', '-n', nargs='?', const=None, help='Target speaker name')

    # detect character code
    with open(parser.parse_args().target, 'rb') as f:
        char_code = chardet.detect(f.read()).get('encoding')

    with open(parser.parse_args().target, encoding=char_code, errors='ignore') as fin:
        input_list = fin.readlines()

    # reshape_texts
    output = get_reshaped_texts(input_list, parser)

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


