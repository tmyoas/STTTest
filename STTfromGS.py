import datetime
import os
import argparse
import codecs
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

import EvaluateSTT


def transcribe_gcs(gcs_uri, hint_phrases, set_config):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech_v1p1beta1.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)

    # hint_phrase = []
    # set_config['enable_speaker_diarization'] = 'False'

    # Set default values, check dict having each key and cast from str to each type.
    config = types.RecognitionConfig(
        encoding=eval(set_config.get('encoding', 'enums.RecognitionConfig.AudioEncoding.FLAC')),
        sample_rate_hertz=int(set_config.get('sample_rate_hertz', 16000)),
        language_code=set_config.get('language_code', 'en-US'),
        enable_automatic_punctuation=eval(set_config.get('enable_automatic_punctuation', True)),
        enable_speaker_diarization=eval(set_config.get('enable_speaker_diarization', False)),
        diarization_speaker_count=int(set_config.get('diarization_speaker_count', 1)),
        speech_contexts=[speech_v1p1beta1.types.SpeechContext(phrases=hint_phrases)])

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)
    return response


def get_stringlist_from_file(path):
    str_list = []
    f = open(path, 'r')
    for line in f:
        str_list.append(line.rstrip())
    f.close()
    return str_list


def get_hashmap_from_file(path):
    hashmap = {}
    f = open(path, 'r')
    for line in f:
        tmp = line.rstrip().split("=")
        hashmap[tmp[0]] = tmp[1]
    f.close()
    return hashmap


def get_transcription_from_response(response, is_compare = False):
    result_max_index = len(response.results) - 1

    timestamp = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    fout = codecs.open('transcribe{}.txt'.format(timestamp), 'a', 'UTF-8')

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    if is_compare:
        for index, result in enumerate(response.results):
            # The first alternative is the most likely one for this portion.
            alternative = result.alternatives[0]
            # Sometime transcript added "." even if enable_speaker_punctuation=False.
            fout.write(u'{}'.format(alternative.transcript.rstrip(".")))
        fout.close()
    else:
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
    return 0


if __name__ == '__main__':
    # Setting of command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('gspath', help='A Google Cloud Storage path with .flac file')
    parser.add_argument('--compare', '-c', action="store_true", help='Output mode (Just result or add confidence, speaker_tag, and so on.)')

    HINT_FILE = './resources/hint_list'
    hints = []
    if os.path.isfile(HINT_FILE):
        hints = get_stringlist_from_file(HINT_FILE)

    CONFIG_FILE = './resources/recognition_config'
    config = {}
    if os.path.isfile(CONFIG_FILE):
        config = get_hashmap_from_file(CONFIG_FILE)

    is_compare = None
    if parser.parse_args().compare:
        is_compare = True
    else:
        is_compare = False

    get_transcription_from_response(transcribe_gcs(parser.parse_args().gspath, hints, config), is_compare)

