import json
import os.path

import requests


def qa_model(content, type: [1, 3] = 1):
    host = '120.133.63.166'
    port = '8006'
    url = f"http://{host}:{port}/v1/chat/completions"
    payload = get_payload(content, type)
    headers = {'Content-Type': 'application/json', 'Host': '120.133.63.166:5001'}
    response = requests.request("POST", url, headers=headers, data=payload)
    for choice in json.loads(response.text).get('choices'):
        content = choice.get('message').get('content')
    # print(response.text)
    print(content.replace('\n\n', ''), '\n')
    return content.replace('小节编写内容:\n', '小节编写内容:').replace('小节编写内容:\n\n', '小节编写内容:')


def get_payload(content, type):
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "stream": False,
        "max_tokens": 4096,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": "根据示例回答问题\n－－－－－－－\n示例:\nHuman: 参考以下文本回答问题：\n－－－－－－－\n文本:\n应收账款自动化软件是一种企业信息化管理软件，主要用于管理企业的应收账款业务。该软件通过自动化处理应收账款的业务流程，帮助企业实现应收账款的高效管理\n－－－－－－－\n问题:\n1. 编写报告中的某个段落,最多200字\n报告名称:中国应收账款自动化软件行业市场深度研究及发展前景投资可行性分析报告(2019年)\n段落名称:应收账款自动化软件行业界定和分类\n小节名称:行业定义、基本概念\n2. 返回固定格式:小节名称:行业定义、基本概念\n内容来源:中国财务网[http://www.caiwu.com]\n小节编写内容:\n－－－－－－－\nAI:小节名称:行业定义、基本概念\n小节编写内容:应收账款自动化软件是一种企业信息化管理软件，主要用于管理企业的应收账款业务。该软件通过自动化处理应收账款的业务流程，帮助企业实现应收账款的高效管理，提高企业的资金使用效率，降低企业的经营风险。应收账款自动化软件的基本功能包括：应收账款的账龄分析、应收账款的预警管理、应收账款的催收管理、应收账款的对账管理等。通过使用应收账款自动化软件，企业可以实现应收账款的智能化管理，提高企业的管理水平，提升企业的经营效益,加快企业企业数字化转型。大概800字左右"
            },
            {
                "role": "user",
                # "content": "参考以下文本回答问题：\n－－－－－－－\n文本:\n\n－－－－－－－\n问题:\n1. 编写报告中的某个小节\n报告名称:全球数字治理发展报告\n段落名称:结论与建议\n小节名称:研究总结与主要发现\n2. 返回固定格式:小节名称:\n内容来源:\n小节编写内容:"
                "content": content
            }
        ]
    })
    if type == 3:
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "stream": False,
            "max_tokens": 4096,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        })
    return payload


def get_question(title, p, s):
    print(title, p, s)
    return f"参考以下文本回答问题：\n－－－－－－－\n文本:\n\n－－－－－－－\n问题:\n1. 编写报告中的某个小节\n报告名称:{title}\n段落名称:{p}\n小节名称:{s}\n2. 返回固定格式:小节名称:\n内容来源:\n小节编写内容:"


def read_txt(q_file):
    file_path = f'../app/qa/{q_file}'
    a_file = os.path.basename(file_path).replace('q', 'a')
    a_file_path = os.path.join(os.path.dirname(file_path), a_file).replace('txt', 'csv')
    f1 = open(a_file_path, 'w', encoding='GBK')
    with open(file_path, 'r', encoding='utf-8') as f:
        title = None
        p = ''
        for line in f:
            if title is None:
                title = line.replace('\n', '')
                continue
            if line.startswith('###'):
                break
            if line.startswith('#'):
                continue
            if not line.startswith('\t'):
                p = line.split(' ')[1].split('\t')[0]
            else:
                s = line.split(' ')[1].split('\t')[0]
                content = get_question(title, p, s)
                result = qa_model(content).replace('\n', '')
                f1.write(f'{title},{p},{s},{result}\n')
        f1.close()


def read_txt_3(q_file):
    file_path = f'../app/qa/{q_file}'
    a_file = os.path.basename(file_path).replace('q', 'a')
    a_file_path = os.path.join(os.path.dirname(file_path), a_file).replace('txt', 'csv')
    f1 = open(a_file_path, 'w', encoding='GBK')
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            result = qa_model(line, 3).replace('\n', '')
            f1.write(f'{line},{result}\n')
        f1.close()


def outline():
    data = {}
    subject = data.get('subject', '中国自行车发展行业研究报告')
    keyword = data.get('keyword', '自行车')  # 关键字
    industry = data.get('industry', '车辆')  # 行业
    total_words = data.get('total_words', 10000)
    ip = data.get('ip', '')

    from outline.CreateOutline import CreateOutline
    outline_data = {}
    outline = CreateOutline()
    try:
        outline_data = outline.create_outline(subject, keyword, industry, total_words, ip)
        if outline_data['code'] == 200:
            try:
                outline_data = json.loads(outline_data['outline'])
            except Exception as e:
                print('Error: Failed to decode JSON from outline data')
        else:
            print(f'Error: Failed to fetch outline data. Status code: {outline_data.status_code}')
    except Exception as e:
        print(f'Error: Failed to fetch outline data. {str(e)}')
    print(f'chat-process: outline_data={outline_data}')


if __name__ == '__main__':
    q_file = '全球数字治理-q.txt'
    # read_txt(q_file)
    read_txt_3()
