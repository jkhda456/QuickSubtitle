import os
import sys
import datetime
import argparse
import tempfile
from pathlib import Path

VERSION = '1.0'

MODEL_WHISPER = 'large-v2'
MODEL_NLLB200 = 'facebook/nllb-200-distilled-600M'


def drop_voice_file(target, dest):
	import ffmpeg

	stream = ffmpeg.input(target).output(dest, format='wav', acodec='pcm_s16le', ac=1, ar='16k')
	
	ffmpeg.run(stream, overwrite_output=True)
	
	return dest


def process_whisper(target, def_device="cuda"):
	from faster_whisper import WhisperModel

	model = WhisperModel(MODEL_WHISPER, device=def_device, compute_type="float16")
	segments, info = model.transcribe(target, beam_size=5)
	
	print("Whisper Ready!")
	print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

	cnt = 0
	return_list = []
	
	
	print("start dictation")
	for segment in segments:
		print(cnt)
		cnt += 1
		
		start_date = datetime.datetime(1, 1, 1)
		delta = datetime.timedelta(seconds=segment.start)
		stime = start_date + delta
		
		delta = datetime.timedelta(seconds=segment.end)
		etime = start_date + delta
		
		end_time = datetime.timedelta(seconds=segment.end)

		print("%s -> %s\n%s\n" % (stime.strftime('%H:%M:%S,%f')[:-3], etime.strftime('%H:%M:%S,%f')[:-3], segment.text.strip()))
		return_list.append((stime.strftime('%H:%M:%S,%f')[:-3], etime.strftime('%H:%M:%S,%f')[:-3], segment.text.strip()))

	return return_list


def process_nllb(dictation_list, def_src_lang, def_tgt_lang):
	from transformers import pipeline

	if not def_src_lang:
		def_src_lang = 'jpn_Jpan'
	if not def_tgt_lang:
		def_tgt_lang = 'kor_Hang'

	translator = pipeline('translation', model=MODEL_NLLB200, device=0, src_lang=def_src_lang, tgt_lang=def_tgt_lang, max_length=512)
	print("nllb200 Ready!")

	cnt = 0
	trans_list = []
	for data in dictation_list:
		print(cnt)
		cnt += 1
		
		output = translator(data[2], max_length=512)
		line = output[0]['translation_text']
		print("%s -> %s\n%s\n" % (data[0], data[1], line))
		trans_list.append((data[0], data[1], line))

	return trans_list


def main(target):
	#from transformers import pipeline

	print('start Quick Subtitle %s' % VERSION)
	print('target : %s' % target.media_file)
	if not os.path.isfile(target.media_file):
		raise Exception("file not exists..")

	# check ffmpeg executable.

	if not target.skip_convertaudio:
		temp_file = str(Path(target.media_file).with_suffix('.wav'))
		if os.path.isfile(temp_file):
			print("convert file alreay exists, i'll try this file %s" % temp_file)
		else:
			print('convert file : %s ' % temp_file)
			
			# step 1 - convert
			temp_file = drop_voice_file(target.media_file, temp_file)
	else:
		temp_file = target.media_file

	# step 2 - dictation
	dictation_list = process_whisper(temp_file)

	# step 3 - translate
	if not target.skip_translate:
		print("start translate...")
		dictation_list = process_nllb(dictation_list, target.original, target.translate)

	# write srt.
	if target.output:
		with open(target.output, 'w', encoding='utf-8') as f:
			print("save output srt : %s " % target.output)
			
			cnt = 0
			for data in dictation_list:
				f.write("%d\n%s -> %s\n%s\n" % (cnt, data[0], data[1], data[2]))
				cnt += 1




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='AI Quick Subtitle')
	parser.add_argument('media_file', type=str, help='source media file')
	parser.add_argument('--skip-convertaudio', '-A', '-a', action='store_true', help='skip convert audio')
	parser.add_argument('--skip-translate', '-R', '-r', action='store_true', help='skip translate')

	parser.add_argument('--output', '-O', '-o', help='output subtitle (SRT)')

	parser.add_argument('--original', '-L', '-l', help='original language [Default - jpn_Jpan]')
	parser.add_argument('--translate', '-T', '-t', help='language to translate [Default - kor_Hang]')
	
	# parser.add_argument('--print language table', '-P', '-p', action='store_true', help='print language tables')

	args = parser.parse_args()

	main(args)
