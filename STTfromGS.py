import argparse
import datetime
import io
import sys
import argparse
import codecs


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)

    timestamp = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    fout = codecs.open('transcribe{}.txt'.format(timestamp), 'a', 'UTF-8')
    # fout.write('Transcript, Confidence\n')

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        # print('Confidence: {}'.format(result.alternatives[0].confidence))
        fout.write(u'{}\n'.format(result.alternatives[0].transcript))
        # fout.write('{}\n'.format(result.alternatives[0].confidence))
    fout.close()

# def fout_with_timestamp(output, timestamp):
#     fout = codecs.open('transcribe{}.txt'.format(timestamp), 'a', 'UTF-8')
#     fout.write(u'{}'.format(output.transcript))
#     fout.write(u'{}\n'.format(output.confidence))


if __name__ == '__main__':
    # Setting of command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('gspath', help='A Google Cloud Storage path with .flac file')
    transcribe_gcs(parser.parse_args().gspath)
