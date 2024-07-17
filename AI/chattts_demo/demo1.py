import ChatTTS


chat = ChatTTS.Chat()
chat.load_models(compile=False) # 设置为True以获得更快速度

texts = ["在这里输入你的文本",]

wavs = chat.infer(texts, use_decoder=True)
# torchaudio.save("output1.wav", torch.from_numpy(wavs[0]), 24000)