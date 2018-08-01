from gtts import gTTS

def make_tts(input):

	print("==========================start write")
	tts_kr = gTTS(input, lang='ko')

	filename = input[:9].replace(' ','')

	print("==========================filename"+filename)
	with open('./static/audio/'+filename+'.mp3', 'wb') as f:
	     tts_kr.write_to_fp(f)

	print("==========================end write")