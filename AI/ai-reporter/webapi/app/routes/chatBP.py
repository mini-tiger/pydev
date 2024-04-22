import base64
from urllib.parse import quote

from flask import Blueprint, request, Response, jsonify
from webapi.service.generate_doc import generator
from webapi.service.json_loop import *

from outline.CreateOutline import CreateOutline
from webapi.service.semaphore import global_api_pool
chatBP = Blueprint('chatBP', __name__, url_prefix='/api')


def generate_sleep():
    time.sleep(config.BaseConfig.GENERATE_SLEEP)



def producer(data_queue, request_body, outline,start_time):
    if outline['title'] == '测试-中国自行车发展行业研究报告':
        for item in outline['Sections']:
            for child_item in item['child']:
                match = re.search(r"^第(\S+)章", item['Section'])
                chapter = ''
                if match:
                    chapter = '第%s章' % match.group(1)

                sub_match = re.search(r'^第(\S+)节', child_item["Section"])
                sub_chapter = ''
                sub_chapter_title = ''
                if sub_match:
                    sub_chapter = '第%s小节' % sub_match.group(1)
                    sub_chapter_title = re.sub(r'^第(\S+)节 ', '', child_item['Section'])

                data_queue.put(json.dumps({
                    'index': 'outline_%d_%d' % (item['index'], child_item['index']),
                    'content': f'接口调用：{chapter}{sub_chapter}生成完毕',
                    'sub_content': f'章节标题：“{sub_chapter_title}”',
                    'status': 'finish',
                    'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                }))
    else:
        logger.info(f'chat-process: 开始生成正文')

        result_json = generate_data_json(data_queue, json_obj=outline, request_body=request_body, ip=request_body['ip'],start_time=start_time)
        data_queue.put('<REPORT_GENERATION_COMPLETED>%s' % json.dumps(result_json, indent=4, ensure_ascii=False))
        # if get_current_semaphore():
        #     ip = acquire_semaphore()  # 申请IP
        #     result_json = generate_data_json(data_queue, json_obj=outline, request_body=request_body, ip=ip)
        #     data_queue.put('<REPORT_GENERATION_COMPLETED>%s' % json.dumps(result_json, indent=4, ensure_ascii=False))
        #     release_semaphore(ip)
        # else:
        #     data_queue.put(None)

    # 向数据队列添加一个特殊的“停止”标志，以通知消费者线程退出循环
    data_queue.put(None)


# def consumer(data_queue, result_queue):
#     while True:
#         data = data_queue.get()  # 从队列中获取数据
#         if data is None:  # 如果获取到的数据为None，则退出循环
#             result_queue.put(None)
#             break
#         result_queue.put(data)  # 将消费的数据放入结果队列


@chatBP.route('chat-industry-options', methods=['POST'])
def chat_industry_options():
    try:
        # download_url = config.BaseConfig.DOWNLOAD_URL + file_name
        # # 对 download_url 进行 Base64 编码
        # download_url_base64 = base64.b64encode(download_url.encode()).decode()
        # # 对 Base64 编码后的 URL 进行 URL 编码
        # encoded_download_url = quote(download_url_base64)
        # view_url = config.BaseConfig.VIEW_URL.replace('${url}', encoded_download_url)

        outline = CreateOutline()
        report_type = outline.getReportType()
        industry_options = report_type[0]
        template_view_url_options = report_type[1]
        new_industry_options = []
        for item in industry_options:
            view_url = ''
            if item in template_view_url_options and item != '智能生成':
                download_url = config.BaseConfig.DOWNLOAD_URL + template_view_url_options[item]
                # logger.info(f'chat-industry-options: item={item}')
                # logger.info(f'chat-industry-options: download_url={download_url}')
                # 对 download_url 进行 Base64 编码
                download_url_base64 = base64.b64encode(download_url.encode()).decode()
                # 对 Base64 编码后的 URL 进行 URL 编码
                encoded_download_url = quote(download_url_base64)
                view_url = config.BaseConfig.VIEW_URL.replace('@replace@', encoded_download_url)
            new_industry_options.append({
                'option': item,
                'view_url': view_url
            })

        return jsonify({'status': 'success', 'message': '', 'data': {'industry_options': industry_options, 'new_industry_options': new_industry_options}})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None})


@chatBP.route('chat-info', methods=['POST', 'GET'])
def chat_info():
    try:
        config_json=os.path.join(config.BaseConfig.base_dir, "config.json")
        logger.info(config_json)
        # 打开JSON文件并加载数据
        with open(config_json, 'r') as file:
            data = json.load(file)

        return jsonify({'status': 'success', 'message': '', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None})


@chatBP.route('chat-industry', methods=['POST'])
def chat_industry():
    try:
        # 获取 POST 请求中的参数
        data = request.json
        subject = data['subject']

        outline = CreateOutline()
        industry = outline.checkReportType(subject)
        return jsonify({'status': 'success', 'message': '', 'data': {'industry': json.loads(industry)['classify']}})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None})


@chatBP.route('chat-keyword', methods=['POST'])
def chat_keyword():
    try:
        # 获取 POST 请求中的参数
        data = request.json
        subject = data['subject']

        outline = CreateOutline()
        keyword = outline.checkKeyWord(subject)
        if keyword['isNeedKeyWord']:
            return jsonify(
                {'status': 'success', 'message': '', 'data': {'keyword': {'isNeedKeyWord': keyword['isNeedKeyWord']}}})
        else:
            return jsonify({'status': 'success', 'message': '', 'data': {
                'keyword': {'isNeedKeyWord': keyword['isNeedKeyWord'], 'keyword': keyword['keyword']}}})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'data': None})


def sse_response_generator(data):
    subject = data.get('subject', '中国自行车发展行业研究报告')
    keyword = data.get('keyword', '自行车')
    industry = data.get('industry', '车辆')
    total_words = data.get('total_words', 10000)
    test_mode = data.get('test_mode', False)
    ip = data.get('ip', '')
    version = data.get('version', '中咨')
    logger.info(f'chat-process: subject={subject}, keyword={keyword}, industry={industry}, total_words={total_words}, test_mode={test_mode}')

    normal_index = 0
    # 开始生成报告
    yield 'data: %s\n\n' % '{"action": "new", "index": "normal_%d", "title": "接口调用：开始生成报告", "status": "generating", "time": "%s"}' % (normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    generate_sleep()
    normal_index += 1

    # 报告大纲生成中
    yield 'data: %s\n\n' % '{"action": "new", "index": "normal_%d", "title": "接口调用：报告大纲生成中", "status": "generating", "time": "%s"}' % (normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    generate_sleep()

    start_time = time.time()
    outline_data = {}
    outline = CreateOutline()
    err_dagang_str= None
    total_counts = 0
    try:
        logger.info(f"{'==' * 15}--开始生成大纲-{subject}-目录--{'==' * 15}")
        logger.info(f"subject:{subject}, keyword:{keyword}, industry:{industry}, total_words:{total_words}, ip:{ip}")
        outline_data = outline.create_outline(subject, keyword, industry, total_words, ip)
        if outline_data['code'] == 200:
            try:
                outline_data = json.loads(outline_data['outline'])

                for item in outline_data['Sections']:
                    total_counts += len(item['child'])
            except Exception as e:
                err_dagang_str=f'Error: Failed to decode JSON from outline data,{str(e)}'
        else:
            err_dagang_str=f'Error: Failed to fetch outline data. Status code: {outline_data.status_code}'

    except Exception as e:
        # logger.error(f'Error: Failed to fetch outline data Error: {str(e)}')
        err_dagang_str=f'Error: Failed to fetch outline data Error: {str(e)}'

    if err_dagang_str is not None:
        yield 'data: %s\n\n' % '{"action": "error", "index": "normal_%d", "content": "%s", "status": "error", "time": "%s"}' % (normal_index,err_dagang_str, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        logger.error(err_dagang_str)
        global_api_pool.release_ip(ip)
        return

    logger.info(f'chat-process: outline_data={json.dumps(outline_data,indent=2,ensure_ascii=False)}')
    # # TODO: 如果生成失败直接返回给前端
    # if len(outline_data) == 0:
    #     pass

    logger.info(f"{'==' * 15}--{subject}--生成大纲目录 finish--{'==' * 15}")
    # 报告大纲生成完毕
    yield 'data: %s\n\n' % '{"action": "update", "index": "normal_%d", "content": "接口调用：报告大纲生成完毕", "status": "finish", "time": "%s", "totalCounts": %d}' % (normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), total_counts)
    generate_sleep()
    normal_index += 1

    # 文本摘要提取
    yield 'data: %s\n\n' % '{"action": "new", "index": "normal_%d", "content": "接口调用：文本摘要提取，调用成功！", "sub_content": "报告标题：《%s》", "status": "finish","time": "%s"}' % (normal_index, outline_data['title'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    generate_sleep()
    normal_index += 1

    # for i in range(len(outline_data['Sections'])):
    #     match = re.match(r'^第(\S+)章', outline_data['Sections'][i]['Section'])
    #     chapter = ''
    #     # chapter_title = ''
    #     if match:
    #         chapter = '第%s章' % match.group(1)
    #         # chapter_title = re.sub(r'^第(\S+)章 ', '', outline_data['Sections'][i]['Section'])
    #     for j in range(len(outline_data['Sections'][i]['child'])):
    #         sub_match = re.match(r'^第(\S+)节', outline_data['Sections'][i]['child'][j]['Section'])
    #         sub_chapter = ''
    #         sub_chapter_title = ''
    #         if sub_match:
    #             sub_chapter = '第%s小节' % sub_match.group(1)
    #             sub_chapter_title = re.sub(r'^第(\S+)节 ', '', outline_data['Sections'][i]['child'][j]['Section'])
    #         yield 'data: %s\n\n' % '{"action": "new", "index": "outline_%d_%d", "content": "接口调用：%s%s生成中", "sub_content": "章节标题：“%s”", "status": "generating", "time": "%s"}' % (outline_data['Sections'][i]['index'], outline_data['Sections'][i]['child'][j]['index'], chapter, sub_chapter, sub_chapter_title, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    #         generate_sleep()

    data_queue = queue.Queue()  # 创建一个先进先出（FIFO）队列
    # result_queue = queue.Queue()  # 创建一个队列用于存放消费结果

    # 创建生产者线程
    producer_thread = threading.Thread(target=producer, args=(data_queue, {
        'subject': subject,
        'keyword': keyword,
        'industry': industry,
        'total_words': total_words,
        'test_mode': test_mode,
        'ip': ip,
    }, outline_data, start_time,))
    producer_thread.start()

    # 创建消费者线程
    consumer_thread = threading.Thread()
    consumer_thread.start()

    all_result = {}
    while True:
        logger.info(f'chat-process: 开始消费，等待数据入队')
        result = data_queue.get()
        logger.info(f'chat-process: data_queue.get={result}')
        if subject == '测试-中国自行车发展行业研究报告':
            if result is None:
                break
            else:
                result_map = json.loads(result)
                yield 'data: %s\n\n' % '{"action": "new", "index": "%s", "content": "%s", "sub_content": "%s", "status": "generating", "time": "%s"}' % (
                result_map['index'], result_map['content'], result_map['sub_content'],
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                generate_sleep()
                yield 'data: %s\n\n' % '{"action": "update", "index": "%s", "content": "%s", "sub_content": "%s", "status": "finish", "time": "%s"}' % (
                result_map['index'], result_map['content'], result_map['sub_content'],
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                generate_sleep()
        else:
            if result is None:
                break
            if result.startswith('<REPORT_GENERATION_COMPLETED>'):
                all_result = json.loads(result[29:])
            else:
                result_map = json.loads(result[6:])

                match = re.search(r"第(\S+)章", result_map['content'])
                chapter = ''
                if match:
                    chapter = '第%s章' % match.group(1)

                sub_match = re.search(r'\[第(\S+)节\s+(\S+)\]', result_map['content'])
                sub_chapter = ''
                sub_chapter_title = ''
                if sub_match:
                    sub_chapter = '第%s小节' % sub_match.group(1)
                    sub_chapter_title = sub_match.group(2)

                if result_map['action'] == 'new':
                    yield 'data: %s\n\n' % '{"action": "new", "index": "%s", "content": "接口调用：%s%s生成中", "sub_content": "章节标题：“%s”", "status": "generating", "time": "%s"}' % (result_map['index'], chapter, sub_chapter, sub_chapter_title, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                    generate_sleep()
                else:
                    yield 'data: %s\n\n' % '{"action": "update", "index": "%s", "content": "接口调用：%s%s生成完毕", "sub_content": "章节标题：“%s”", "status": "finish", "time": "%s"}' % (result_map['index'], chapter, sub_chapter, sub_chapter_title, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                    generate_sleep()

    # 等待消费者线程结束
    consumer_thread.join()
    # 等待生产者线程结束
    producer_thread.join()

    if subject == '测试-中国自行车发展行业研究报告':
        # 报告合并
        yield 'data: %s\n\n' % '{"action": "new", "index": "normal_%d", "content": "接口调用：开始合并报告", "status": "generating", "time": "%s"}' % (
        normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        generate_sleep()

        file_path = os.path.join(config.BaseConfig.current_directory,'/app/attachments/','中国自行车发展行业研究报告.docx')
        # file_name = str.replace(file_path, '../app/attachments/', '')
        file_name = os.path.basename(file_path)
        logger.info(f"download file path:{file_path}")
        logger.info(f"download file name:{file_name}")
        download_url = config.BaseConfig.DOWNLOAD_URL + file_name
        logger.info(f"download url:{download_url}")
        # 对 download_url 进行 Base64 编码
        download_url_base64 = base64.b64encode(download_url.encode()).decode()
        # 对 Base64 编码后的 URL 进行 URL 编码
        encoded_download_url = quote(download_url_base64)
        view_url = config.BaseConfig.VIEW_URL.replace('@replace@', encoded_download_url)
        logger.info(f"view url:{view_url}")
        yield 'data: %s\n\n' % '{"action": "update", "index": "normal_%d", "content": "接口调用：报告合并完毕", "status": "finish", "time": "%s"}' % (
        normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        generate_sleep()
        normal_index += 1
    else:
        file_path = ''
        download_url = ''
        view_url = ''
        if len(all_result) > 0:
            # 报告合并
            yield 'data: %s\n\n' % '{"action": "new", "index": "normal_%d", "content": "接口调用：开始合并报告", "status": "generating", "time": "%s"}' % (normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            generate_sleep()
            try:

                logger.info(f"开始合并报告{outline_data['title']}")
                file_path = generator(outline_data['title'], all_result, version)
            except Exception as e:
                logger.error(e.__str__())
            logger.info(f"!!!!文件生成完毕 file path:{file_path}")
            file_name = file_path.split(os.path.sep)[-1]
            # file_name = str.replace(file_path, '../app/attachments/', '')
            download_url = config.BaseConfig.DOWNLOAD_URL + file_name
            logger.info(f"download url:{download_url}")
            # 对 download_url 进行 Base64 编码
            download_url_base64 = base64.b64encode(download_url.encode()).decode()
            # 对 Base64 编码后的 URL 进行 URL 编码
            encoded_download_url = quote(download_url_base64)
            # logger.info(f"env VIEW_URL:{config.BaseConfig.VIEW_URL}")
            view_url = config.BaseConfig.VIEW_URL.replace('@replace@', encoded_download_url)
            logger.info(f"view url:{view_url}")
            yield 'data: %s\n\n' % '{"action": "update", "index": "normal_%d", "content": "接口调用：报告合并完毕", "status": "finish", "time": "%s"}' % (normal_index, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            generate_sleep()
            normal_index += 1

    # 报告生成完毕
    yield 'data: %s\n\n' % '{"action": "update", "index": "normal_0", "title": "接口调用：报告生成完毕", "status": "finish", "time": "%s"}' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    generate_sleep()

    yield 'data: %s\n\n' % '{"action": "end", "index": "normal_%d", "file_path": "%s", "title": "%s", "download_url": "%s", "view_url": "%s", "status": "finish", "time": "%s"}' % (normal_index, file_path, outline_data['title'], download_url, view_url, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    generate_sleep()
    normal_index += 1
    logger.info(f"chat release ip:{ip}")
    global_api_pool.release_ip(ip)
    yield '---end---'


@chatBP.route('chat-free', methods=['POST'])
def chat_free():
    ip = ''
    free = False
    if global_api_pool.get_available_ips():
        ip = global_api_pool.acquire_ip() # 申请IP
        free = True
    logger.info(f"chat get ip:{ip}")
    return jsonify({'status': 'success', 'message': '', 'data': {'ip': ip, 'free': free}})


@chatBP.route('chat-release', methods=['POST'])
def chat_release():
    try:
        logger.info(f'chat-release: 开始释放IP，释放IP为：{request.json["ip"]}')
        # 获取 POST 请求中的参数
        data = request.json
        ip = data['ip']

        global_api_pool.release_ip(ip)

        return jsonify({'status': 'success', 'message': '', 'data': None})
    except Exception as e:
        logger.error(f"chat release err:{str(e)}:{request.json}")
        return jsonify({'status': 'error', 'message': str(e), 'data': None})

@chatBP.route('chat-process', methods=['POST'])
def chat_process():
    data = request.json
    return Response(sse_response_generator(data), mimetype='text/event-stream')

@chatBP.route('health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@chatBP.route('test-loop', methods=['POST'])
def chat_test_loop():
    ip = ''
    free = False
    if global_api_pool.get_available_ips():
        ip = global_api_pool.acquire_ip()  # 申请IP
        free = True
    print(f"!!!!!! IP: {ip}")
    outline_data = {}
    outline = CreateOutline()

    try:
        outline_data = outline.create_outline(subject='全球数字治理研究报告', keyword='', type='智能生成', words_amount='10000', base_url=ip)
        logger.info(json.dumps(outline_data,ensure_ascii=False, indent=2))
        if outline_data['code'] == 200:

            data_queue = queue.Queue()
            try:
                outline_data = json.loads(outline_data['outline'])
                request_body = {'subject': '全球数据治理研究报告',
                                'keyword': '', 'industry': '智能生成',
                                'total_words': 10000, 'test_mode': False,
                                'ip': ip}
                result_json = generate_data_json(data_queue, json_obj=outline_data, request_body=request_body,
                                                                                            ip=ip,start_time=time.time())
                version = request_body.get('version', '中咨')
                file_path = generator(outline_data['title'], result_json,version)
                print(f"!!!!!! finish {file_path}")
                global_api_pool.release_ip(ip)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f'Error: Failed to decode JSON from outline data:{str(e)}')

    except Exception as e:
        import traceback
        traceback.print_exc()
    return jsonify({'status': 'success', 'message': '', 'data': {'ip': ip, 'free': free}})