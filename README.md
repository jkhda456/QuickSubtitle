# QuickSubtitle
Quick Subtitle using AI


## Quickstart

 1. install packages
   1. whisper : https://github.com/guillaumekln/faster-whisper
   2. pytorch : https://pytorch.org/get-started/locally
   3. transformers : https://github.com/huggingface/transformers
   4. ffmpeg-python : https://github.com/kkroening/ffmpeg-python
 2. download ffmpeg or add to path
 3. run Quick.py!

## how to use

```
python Quick.py [target media file] -o [output srt file]
```


```
usage: Quick.py [-h] [--skip-convertaudio] [--skip-translate] [--output OUTPUT] [--original ORIGINAL]
                [--translate TRANSLATE]
                media_file

AI Quick Subtitle

positional arguments:
  media_file            source media file

options:
  -h, --help            show this help message and exit
  --skip-convertaudio, -A, -a
                        skip convert audio
  --skip-translate, -R, -r
                        skip translate
  --output OUTPUT, -O OUTPUT, -o OUTPUT
                        output subtitle (SRT)
  --original ORIGINAL, -L ORIGINAL, -l ORIGINAL
                        original language [Default - jpn_Jpan]
  --translate TRANSLATE, -T TRANSLATE, -t TRANSLATE
                        language to translate [Default - kor_Hang]
```
