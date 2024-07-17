

import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-zRD1uWX3Kmam5TDmDe9952Cb001c41EeB3059974C0Ec2eF1",
    base_url="http://172.22.220.89:3001/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-32k",
    messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
    ],
    temperature=0.3,
)

print(completion.choices[0].message.content)