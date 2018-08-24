import datetime
import os
import argparse
import codecs
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

def transcribe_gcs(gcs_uri, hint_phrases):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech_v1p1beta1.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=3,
        speech_contexts=[speech_v1p1beta1.types.SpeechContext(phrases=hint_phrases)])

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=9000)
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
    # TODO: Convert each line(aaa=bbb) in file to hashmap({'aaa':'bbb'})
    hashmap = {}
    return hashmap

def get_config_from_hashmap(config):
    # TODO: Fill shortage config and return types.RecognitionConfig()
    return types.RecognitionConfig()


if __name__ == '__main__':
    # Setting of command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('gspath', help='A Google Cloud Storage path with .flac file')

    HINT_FILE = './resources\hint_list'
    hints = []
    if os.path.isfile(HINT_FILE):
        hints = get_Stringlist_from_file(HINT_FILE)

    # CONFIG_FILE = './resources\config'
    # config = {}
    # if os.path.isfile(CONFIG_FILE):
    #     config = get_Stringlist_from_file(CONFIG_FILE)
    # if len(config) == 0:
    # TODO: Handling if config file is shortage
        
    transcribe_gcs(parser.parse_args().gspath, hints, config)

