from webapi.service.json_loop import *
from outline.CreateOutline import CreateOutline

ip = "http://120.133.63.166:8002/v1"

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
    json_file1 = 'sft.json'
    # result_json=generate_json_sft_single(subject='全球数据治理研究报告')
    # # 打开 JSON 文件并读取数据
    # with open('abc.json', 'r') as file:
    #     data = json.load(file)
    #     result_list = generate_prompt(data,prompt_dict_tpl.get("yi"))
    #     print(json.dumps(result_list,ensure_ascii=False, indent=4))
    result_list_total = []
    for i in ['全球数据治理研究报告','中国数字治理研究报告','当代中国数字治理动态与发展趋向','当今数字治理现状,需求与对策研究','全球数字治理的发展与挑战','数字时代的全球治理架构','数字经济时代的全球治理模式',
            '全球数字治理的政府角色与责任','数字领域中的全球合作与协调','数据隐私保护与全球数字治理','信息安全与全球数字治理','数字金融时代的全球监管挑战','全球数字治理的跨国企业责任','互联网治理与全球数字时代',
            '全球数字治理与公民参与','全球数字化时代的法律与政策协调','数据共享与全球数字治理','数字教育与全球治理','全球数字治理的发展趋势与展望','数字技术对全球卫生治理的影响','全球数字治理与数字就业机会','数字技术对全球贸易与商业的影响',
            '全球数字治理的社会影响与责任','欧美数字治理合作的影响因素及前景分析','数字治理在打击犯罪中的应用','数字治理对公共服务质量的影响','数字治理：实现政府透明度的新途径','数字治理与公共服务的个性化','数字治理在交通管理中的实践',
            '数字治理与公民素质提升','数字治理在防灾减灾中的作用','数字治理的未来：预测与展望','数字技术对全球社会平等与公正的影响趋势研究','全球数字治理中的数据驱动决策趋势与实践案例','数字化时代下全球环境治理的新趋势与应对策略',
              '新兴数字技术对全球教育与人才发展的趋势分析','数字文化遗产保护与全球治理的最新趋势探索','全球数字化时代下数字经济发展的趋势与前景展望','数字技术对全球卫生安全与医疗治理的趋势评估','全球数字治理中的跨国合作与协调趋势分析'
              ]:
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