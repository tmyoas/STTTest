# Using Google Cloud Speech-to-Text

## Repository map
```
<root>
    readme.md
    requirements.txt
    /src
        STTfromGS.py
        EvaluateSTT.py
        ReshapeTexts.py
    /resources
        recognition_config
    /test
        TestSTTfromGS.py
        TestEvaluateSTT.py
        /resources
            stringlist
            hashmap
```

## Overview
### STTfromGS.py
- Input: 
    - Audio file (in your Google Storage)
    - resources/hint_list (Optional)
    - resources/recognition_config (Optional)
- Output:
    - transcribe[YYYYmmdd-HHMMSS].txt
- Usage in console: 
```
# STTfromGS.py <Google Storage address>
```
- Options:
```
--compare , -c : Output file is reshaped for evaluateSTT.py (Only transtribe text). 
```

### EvaluateSST.py
- Input: 
    - Transcription file (text)
    - Answer file (text)
- Output:
    - Word error rate (in console)
- Usage in console: 
```
 # EvaluateSTT.py <Transcription file> <Answer file>
 # WER: <float>
 # ins: <int>, del: <int>, sub: <int>, correct: <int>, words: <int> 
```
- Options:
```
--output <filepath>, -o <filepath>: Output a result with timestamp in selected file. './result_evaluateSTT.txt' is used if you don't set <filepath>.
```

### ReshapeTexts.py
- Input: 
    - <transcript file>.txt (Using STTfromGS.py/Voice Rep Pro 3)
- Output:
    - <transcript file>_reshaped.txt
        - One line, only, result, no punctuation.
- Usage in console: 
```
# ReshapeTexts.py <transcription file>
```
- Options:
```
--output <filepath>, -o <filepath> : You can set output filepath and filename (in default, <transcript file>_reshaped.txt is made the same directory as input file.) 
```
    
    
### resources/hint_list
```
<hint1>
<hint2>
...
```

### recognition_config
```
<config_parameter1>=<Value1>
<config_parameter2>=<Value2>
...
```
config_parameter: Please check official information

## TODO
- Make unit test
- Define how to change '-' in ReshapeTexts.py
- Add reshape option in STTfromGS.py