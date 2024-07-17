import re

def remove_bracket_content(text):
    return re.sub('<[^>]*>', '', text)

# 测试函数
input_text = "<|zh|><|EMO_UNKNOWN|><|Speech|><|withitn|>喂喂喂喂喂嗯你好。"
result = remove_bracket_content(input_text)
print(result)