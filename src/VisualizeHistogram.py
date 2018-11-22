import argparse
import collections
import matplotlib.pyplot as plt
import csv

def get_wordlist_from_file(input_path):
    fin = open(input_path, encoding="utf8")
    words_list = fin.read().split(" ")
    while '' in words_list:
        words_list.remove('')
    fin.close()
    return words_list

def get_hist_dict(target_list):
    hist_dict = collections.Counter(target_list)
    return hist_dict

def show_hist_graph(hist_dict):
    graph_x_list = []
    graph_y_list = []
    hist_dict = sorted(hist_dict.items(), key=lambda i: i[1], reverse=True)
    for key, value in hist_dict:
        graph_x_list.append(key)
        graph_y_list.append(value)
    plt.title('Histogram')
    plt.xlabel('Word')
    plt.ylabel('Freq')
    plt.bar(graph_x_list, graph_y_list)
    plt.show()
    return 0

def output_dict_to_csv(data_dict, filepath='./histogram.csv'):
    # TODO: how to make header
    data_dict = sorted(data_dict.items(), key=lambda i: i[1], reverse=True)
    fieldnames = ('word', 'count')
    with open(filepath, 'w', newline='', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for key, value in data_dict:
            writer.writerow({'word': key, 'count': value})
    return 0

def compare_hist(hist_dict_a, hist_dict_b):
    # hist_dict_a (a in below) : {word(str) : num of appearance(int), ...}
    # hist_dict_b (b in below) : {word(str) : num of appearance(int), ...}
    # hist_dict_compare (c in below) : a - b for each key.
    # If there is no key in a, c's value is a.
    # If there is no key in b. c's value is -b.
    hist_dict_compare = {}
    for key, value in hist_dict_a.items():
        if key in hist_dict_b:
            hist_dict_compare[key] = (hist_dict_a[key] - hist_dict_b[key])
            del hist_dict_b[key]
        else:
            hist_dict_compare[key] = hist_dict_a[key]

    for key, value in hist_dict_b.items():
        hist_dict_compare[key] = -int(hist_dict_b[key])
    return hist_dict_compare

if __name__ == '__main__':
    # Setting of command-line parameters
    # target: a target file that you want to show word-histogram graph
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='A target file to show word-histogram.')

    target_list = get_wordlist_from_file(parser.parse_args().target)
    answer_list = get_wordlist_from_file('transcription.txt')
    hist_dict = get_hist_dict(target_list)
    ans_dict = get_hist_dict(answer_list)
    compare_dict = compare_hist(ans_dict, hist_dict)
    # show_hist_graph(compare_dict)
    output_dict_to_csv(compare_dict)
