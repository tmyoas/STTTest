import argparse
import os
import re
import chardet
import json
import src.ReshapeTexts as rt

if __name__ == '__main__':
    # Setting of command-line parameters
    # target: A file that you want to reshape
    # file: output filepath and filename
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='A reshape-target file.')
    parser.add_argument('output', nargs='?', help='An output file (default: <target filename>_reshaped.txt)')
    parser.add_argument('name', nargs='?', default=None, help='dummy')

    service_name = 'Amazon transcribe'
    if service_name == 'Amazon transcribe':
        input_list = []
        with open(parser.parse_args().target, 'r') as f:
            json_dict = json.load(f)
            input_list.append(json_dict['results']['transcripts'][0]['transcript'])

    # reshape_texts
    output = rt.get_reshaped_texts(input_list, parser)

    # TODO: separate method (make_output_file)
    if not parser.parse_args().output:
        targetpath = os.path.split(parser.parse_args().target)
        outputpath = (targetpath[0], targetpath[1].replace('.json', '_reshaped.txt'))
    else:
        outputpath= os.path.split(parser.parse_args().output)
    os.makedirs(outputpath[0], exist_ok=True)
    fout = open(os.path.join(outputpath[0], outputpath[1]), mode='w', encoding="utf8")
    fout.write(output)
    fout.close()
