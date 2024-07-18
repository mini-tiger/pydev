import os
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_completion():
    client = OpenAI(
        api_key="sk-RggH0r7aumh2RWlUHdMfAGPG9xsMFyN7O4cz0fDyhqYuzhr6",
        base_url="https://api.moonshot.cn/v1",
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
    return completion.choices[0].message.content

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_completion) for _ in range(5)]
        for future in as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"Generated an exception: {e}")

if __name__ == "__main__":
    main()
