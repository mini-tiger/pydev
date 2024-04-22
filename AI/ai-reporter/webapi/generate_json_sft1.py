from webapi.service.json_loop import *
from outline.CreateOutline import CreateOutline

ip = "http://120.133.63.166:8003/v1"



def generate_prompt(result_json,prompt):
    try:
        title =result_json['title']
        result_list = []
        cot_template = prompt.get('cot')
        for v in result_json['Sections']:
            print(v)
            section=v.get('Section')

            for child_v in v['child']:
                q = prompt.get('user').format(vector_text='',
                                              word_batch_size=200,
                                              word_batch_size_extend=300,
                                              title=title, section=section, child_section=child_v['Section'])
                result_list.append({'title':title,
                                    'section':section,
                                    'child_section':child_v['Section'],
                                    'system_prompt':cot_template,
                                    'user_prompt':q,
                                    'unique_prompt': f"报告名称:{title}\n 段落名称:{section}\n 小节名称:{child_v['Section']}",
                                    'chosen':child_v['data']
                                    })
    except Exception as e:
        return []
    return result_list

def generate_json_sft_single(subject='全球数据治理研究报告'):
    result_json = {}
    outline = CreateOutline()
    try:
        outline_data = outline.create_outline(subject=subject, keyword='', type='智能生成', words_amount='10000', base_url=ip)
        data_queue = queue.Queue()

        outline_data = json.loads(outline_data['outline'])
        result_json = generate_data_json(data_queue, json_obj=outline_data,
                                         request_body={'subject': subject,
                                                       'keyword': '', 'industry': '智能生成',
                                                       'total_words': 10000, 'test_mode': False,
                                                       'ip': ip},
                                         ip=ip, start_time=time.time())
        # print(result_json)
    except Exception as e:
        print(e)

    return result_json

if __name__ == '__main__':
    json_file1 = 'sft1.json'
    # result_json=generate_json_sft_single(subject='全球数据治理研究报告')
    # # 打开 JSON 文件并读取数据
    # with open('abc.json', 'r') as file:
    #     data = json.load(file)
    #     result_list = generate_prompt(data,prompt_dict_tpl.get("yi"))
    #     print(json.dumps(result_list,ensure_ascii=False, indent=4))
    result_list_total = []
    for i in ['数字治理对小微企业支持的策略','数字治理与社区建设','大数据在公共服务优化中的应用','互联网治理的最新全球趋势与发展态势分析','社交媒体平台与全球信息治理的新趋势探索',
              '数据驱动型决策与全球治理','数字治理格局研判的理论与方法探索','数字治理平台提升政社共治有效性的多元机制','数字治理中的全球网络安全与威胁应对','数据共享与开放创新的全球数字治理实践']:
        result_json=generate_json_sft_single(subject=i)
        result_list = generate_prompt(result_json, prompt_dict_tpl.get("yi"))
        if len(result_list) == 0:
            continue
        # print(json.dumps(result_list, ensure_ascii=False, indent=4))
        result_list_total.extend(result_list)

    # 将列表写入 JSON 文件
    with open(json_file1, "w") as json_file:
        json.dump(result_list_total, json_file, indent=4, ensure_ascii=False)  # 使用 indent 参数来格式化 JSON 数据

    print(json.dumps(result_list_total, ensure_ascii=False, indent=4))