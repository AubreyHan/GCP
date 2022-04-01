from google.cloud import speech

client = speech.SpeechClient()

audio = speech.RecognitionAudio(uri='gs://hydemo01/demo01.flac')

config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="zh-CN",
    )

response = client.recognize(config=config, audio=audio)

#print (client)