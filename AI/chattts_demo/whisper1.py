import whisper
import whisper
import torch
print(torch.cuda.is_available())    # true 则开启成功
model = whisper.load_model("base")
result = model.transcribe("/mnt/191/033247_use1.07s-audio1.97s-seed11-te0.3-tp0.7-tk20-textlen10-75808.wav", fp16=False, language="Chinese")
print(result["text"])

from openai import OpenAI
client = OpenAI()

audio_file= open("/mnt/191/033247_use1.07s-audio1.97s-seed11-te0.3-tp0.7-tk20-textlen10-75808.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)
print(transcription.text)
# model = whisper.load_model("base")
#
# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("/mnt/191/033247_use1.07s-audio1.97s-seed11-te0.3-tp0.7-tk20-textlen10-75808.wav")
# audio = whisper.pad_or_trim(audio)
#
# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)
#
# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")
#
# # decode the audio
# options = whisper.DecodingOptions()
# result = whisper.decode(model, mel, options)
#
# # print the recognized text
# print(result.text)