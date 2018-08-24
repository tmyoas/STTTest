import datetime
import os
import re
import argparse
import codecs
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

def transcribe_gcs(gcs_uri, hint_phrases, config):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech_v1p1beta1.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=config['encoding'],
        sample_rate_hertz=config['sample_rate_hertz'],
        language_code=config['language_code'],
        enable_automatic_punctuation=config['enable_automatic_punctuation'],
        enable_speaker_diarization=config['enable_speaker_diarization'],
        diarization_speaker_count=config['diarization_speaker_count'],
        speech_contexts=[speech_v1p1beta1.types.SpeechContext(phrases=hint_phrases)])

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)
    result_max_index = len(response.results) - 1

    timestamp = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    fout = codecs.open('transcribe{}.txt'.format(timestamp), 'a', 'UTF-8')

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for index, result in enumerate(response.results):
        # The first alternative is the most likely one for this portion.
        alternative = result.alternatives[0]
        fout.write(u'Transcript: {}\n'.format(alternative.transcript))
        fout.write('Confidence: {}\n'.format(alternative.confidence))
        if index == result_max_index:
            # When last loop, output speaker_tag with each word
            for word_info in alternative.words:
                fout.write('Speaker: {}, '.format(word_info.speaker_tag))
                fout.write(u'Word: {}\n'.format(word_info.word))
    fout.close()

def get_stringlist_from_file(path):
    str_list = []
    f = open(path, 'r')
    for line in f:
        str_list.append(line.rstrip())
    f.close()
    return str_list

def get_hashmap_from_file(path):
    # Default values
    hashmap = {}
    hashmap['encoding'] = enums.RecognitionConfig.AudioEncoding.FLAC
    hashmap['sample_rate_hertz'] = 16000
    hashmap['language_code'] = 'en-US'
    hashmap['enable_automatic_punctuation'] = True
    hashmap['enable_speaker_diarization'] = False
    hashmap['diarization_speaker_count'] = 1

    f = open(path, 'r')
    for line in f:
        tmp = line.rstrip().split("=")
        if tmp[0] == 'encoding' or tmp[0].count('enable'):
            hashmap[tmp[0]] = eval(tmp[1])
        elif tmp[1].isdecimal():
            hashmap[tmp[0]] = int(tmp[1])
        else:
            hashmap[tmp[0]] = tmp[1]
    f.close()
    return hashmap

if __name__ == '__main__':
    # Setting of command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('gspath', help='A Google Cloud Storage path with .flac file')

    HINT_FILE = './resources\hint_list'
    hints = []
    if os.path.isfile(HINT_FILE):
        hints = get_stringlist_from_file(HINT_FILE)

    CONFIG_FILE = './resources/recognition_config'
    config = {}
    if os.path.isfile(CONFIG_FILE):
        config = get_hashmap_from_file(CONFIG_FILE)

    transcribe_gcs(parser.parse_args().gspath, hints, config)
