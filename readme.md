# Using Google Cloud Speech-to-Text

## Repository map
```
<root>
    readme.md
    STTfromGS.py
    EvaluateSTT.py
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