import copy
import queue
import time
import webapi.config
from webapi.template.tpl_data import tpl_json_dict
import json, re
from concurrent.futures import ThreadPoolExecutor
import threading
from webapi.log.setup import logger
from webapi.service.generate_paragraphs import *
import webapi.config as config
# from webapi.db.vector import *
from langchain.globals import set_debug, set_verbose
from webapi.service.large_model_prompt import prompt_dict_tpl
from webapi.service.semaphore import IPPool,global_api_pool
from webapi.utils.progress import progress_bar
set_debug(False)
set_verbose(False)


def computer_word(total, prop):
    # 使用正则表达式提取数字部分
    prop_list = prop.split('%')
    if len(prop_list) < 2:
        number = 2  # default 2%
    else:
        number = float(prop_list[0])
        # print(number)
    word_total = int(total * (number / 100) * config.BaseConfig.WORD_MULTIPLE)
    return word_total, int(word_total * 1.2)


def update_data(json_obj, parent_section, prompt, ip_pool, title_name, total_word, message_queue, status_queue,
                index_section_dict,vectorstore,query_vector_open):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == "data":
                log_section = f'parent_section:{parent_section} ,Section: {json_obj["Section"]},index:{json_obj["index"]}'
                ip = ip_pool[0] if int(config.BaseConfig.GPUOS_PLATFORM) != 1 else ""  # 申请IP
                word_batch_size, word_batch_size_extend = computer_word(total_word, json_obj.get("proportion", 2))
                s_time = time.time()
                url = config.BaseConfig.GPUOS_PLATFORM_URL if int(config.BaseConfig.GPUOS_PLATFORM) == 1 else ip
                # logger.info(
                #     f"Acquired IP: {url} for {log_section} word_batch_size:{word_batch_size} - {word_batch_size_extend}")
                # data_queue.put("开始生成" + log_text)

                log_text = 'data: %s' % '{"action": "new", "index": "outline_%s_%s", "content": "接口调用：章节: [%s] ,小节 [%s] 完成", "status": "process", "time": "%s"}' % (
                    index_section_dict.get(parent_section), json_obj["index"], parent_section, json_obj["Section"],
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                # 开始生成
                logger.info(f"返回sse: {log_text}")
                message_queue.put(log_text)
                source_search_result = ''
                section_data_obj, err = large_model_return_section(ip=ip,
                                                                   word_batch_size=word_batch_size,
                                                                   word_batch_size_extend=word_batch_size_extend,
                                                                   title=title_name,
                                                                   section=parent_section,
                                                                   child_section=json_obj.get("Section"),
                                                                   vectorstore=vectorstore,
                                                                   prompt=prompt,
                                                                   query_vector_open=query_vector_open)
                logger.warning(f"large_model_return_section section_data_obj:{section_data_obj}")
                if err != None:
                    logger.error(
                        f"title:{title_name},section:{parent_section},json_obj:{json_obj},err:{err}, section_data_obj:{section_data_obj}")
                    section_data = ""
                else:
                    section_data = section_data_obj['context']
                    source_search_result = section_data_obj['vectorstore_search_result']

                json_obj[key] = section_data
                json_obj['vectorstore_search_result'] = source_search_result
                json_obj['context_source'] = section_data_obj['context_source']
                # if int(config.BaseConfig.GPUOS_PLATFORM) != 1:
                #     ip_pool.release_ip(ip)  # 释放IP
                log_text_string = json.dumps({
                    "action": "update",
                    "index": f"outline_{index_section_dict.get(parent_section)}_{json_obj['index']}",
                    "recode": section_data,
                    "content": f"接口调用：章节: [{parent_section}] ,小节 [{json_obj['Section']}] 完成",
                    "status": "finish",
                }, indent=2, ensure_ascii=False)
                log_text = f'data: {log_text_string}'
                # 将字典转换为 JSON 字符串
                json_string = json.dumps(json_obj,indent=2, ensure_ascii=False)
                logger.warning(f"返回前端sse: {log_text}")
                message_queue.put(log_text)
                time_consuming = time.time() - s_time
                status_queue.put(time_consuming)
                # logger.info(
                #     f"Released IP: {url} for {log_section},word generate len:{len(section_data)},time:{time_consuming}s")
            elif key == "child":
                for child_item in value:
                    update_data(json_obj=child_item, parent_section=json_obj["Section"], prompt=prompt, ip_pool=ip_pool,
                                title_name=title_name, total_word=total_word, message_queue=message_queue,
                                status_queue=status_queue,
                                index_section_dict=index_section_dict, vectorstore=vectorstore,query_vector_open=query_vector_open)
            else:
                update_data(json_obj=value, parent_section=parent_section, prompt=prompt, ip_pool=ip_pool,
                            title_name=title_name, total_word=total_word, message_queue=message_queue,
                            status_queue=status_queue,
                            index_section_dict=index_section_dict, vectorstore=vectorstore,query_vector_open=query_vector_open)
    elif isinstance(json_obj, list):
        for item in json_obj:
            update_data(json_obj=item, parent_section=parent_section, prompt=prompt, ip_pool=ip_pool,
                        title_name=title_name, total_word=total_word, message_queue=message_queue,
                        status_queue=status_queue,
                        index_section_dict=index_section_dict, vectorstore=vectorstore,query_vector_open=query_vector_open)


def json_data_preprocessing(json_data):
    # 初始化小节计数器
    num_sections = 0

    # 遍历每个章节
    for section in json_data["Sections"]:
        # 将每个章节中的小节数量累加到计数器中
        num_sections += len(section.get("child", []))

    # rebuild json 添加内容来源项
    for section in json_data['Sections']:
        # 遍历每个 Section 下的 child
        for child in section['child']:
            # 添加 source 项
            child['context_source'] = ''
            child['vectorstore_search_result'] = ''

    # 对每个章节按照 index 排序
    sorted_sections = sorted(json_data["Sections"], key=lambda x: x["index"])

    # 对每个章节的子项按照 index 排序
    for section in sorted_sections:
        section["child"] = sorted(section["child"], key=lambda x: x["index"])

    # 返回排序后的 JSON 数据
    return {"title": json_data["title"], "Sections": sorted_sections}, num_sections


# 定义一个函数，用于模拟处理数据的操作
def process_data(time_consuming, num_sections, process_sections, t,start_time,title):
    rate = round( (process_sections / num_sections) * 0.85 + 0.1 , 2 ) # 0.1 是生成目录
    t = t + 10 # 10秒 生成word
    info = progress_bar(title=title,rate=rate,last_time=t,used_time=int(time.time()-start_time))

    print(process_sections,num_sections,info)
    logger.info(f"Finish Processing data 进度: {rate} 剩余时间{t}s,已使用{int(time.time()-start_time)}s")


def process_data_from_queue(data_queue, num_sections,start_time,message_queue,used_time,title):
    process_sections = 0
    time_consuming_his = 0
    while True:
        # 从队列中获取数据，如果队列为空，则阻塞等待直到有数据可用
        time_consuming = data_queue.get()
        # 剩余
        process_sections += 1
        # 总耗时
        time_consuming_his += time_consuming
        # 平均一个需要时间
        avgtime = (time_consuming_his / process_sections)
        process_data(time_consuming, num_sections, process_sections, round(avgtime * (num_sections - process_sections)),start_time,title)


def generate_json_doc(json_data_tpl, title_name, ip_list, total_word, vectorstore, message_queue,start_time,
                      large_model_type="Yi",query_vector_open=1,used_time=15):
    # 将JSON字符串转换为Python字典
    if isinstance(json_data_tpl, str):
        data_dict = json.loads(json_data_tpl)
    else:
        data_dict = json_data_tpl

    # 生成章节与段落序号的字典 日志需要
    index_section_dict = {}
    for value in data_dict["Sections"]:
        index_section_dict.setdefault(value["Section"], value["index"])

    # rebuild json 添加内容来源项,sort
    data_dict, num_sections = json_data_preprocessing(data_dict)

    # online large models
    # ip_pool = IPPool(ip_list=ip_list,msg=title_name)

    # 要更新的数据
    prompt = prompt_dict_tpl.get(large_model_type.lower(), 'yi')

    status_queue = queue.Queue()

    # 创建一个线程，用于状态处理队列中的数据
    processing_thread = threading.Thread(target=process_data_from_queue, args=(status_queue, num_sections,start_time,message_queue,used_time,title_name,))
    processing_thread.start()

    # 使用线程池执行更新操作
    with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
        update_tasks = [
            executor.submit(update_data, section, "", prompt, ip_list, title_name, total_word, message_queue,
                            status_queue,
                            index_section_dict, vectorstore,query_vector_open)
            for section
            in data_dict["Sections"]]
        # 等待所有任务完成
        for task in update_tasks:
            task.result()

    # 打印更新后的JSON数据
    return data_dict


def generate_data_json_request(data_queue, request_body, json_obj, ip_list,start_time, **kwargs):
    total_word = request_body.get("total_words", 500)
    # question = request_body.get("question", "请生成大数据白皮书")
    year = request_body.get("year", 2020)

    # 记录程序开始时间
    start_time = time.time()

    title_type = request_body.get("keyword")
    title_name = json_obj.get("title")
    # data_dict = generate_json_doc(tpl_json_dict['it'], title_name, ip_list, total_word, data_queue)
    vectorstore = None
    # if int(config.BaseConfig.VECTOR_OPEN) == 1:
    #     vectorstore = generate_vector_obj(base_dir=config.BaseConfig.PDF_DIR,
    #                                       vector_index_file=config.BaseConfig.VECTOR_INDEX_FILE)
    if int(config.BaseConfig.VECTOR_OPEN) == 1:
        large_model_type = 'yi_rag'
    else:
        large_model_type = 'yi'

    # if "数据治理" in title_name or "数字治理" in title_name:
    query_vector_open = 1
    # else:
    #     query_vector_open = 0

    data_dict = generate_json_doc(json_obj, title_name, ip_list, total_word, vectorstore,
                                  message_queue=data_queue,
                                  large_model_type=large_model_type,query_vector_open=query_vector_open,start_time=start_time)

    logger.info(f"generate_data_json result: {json.dumps(data_dict, indent=2, ensure_ascii=False)}")
    # 计算程序运行时间
    execution_time = time.time() - start_time

    logger.warning(f"!!!!!! title:{title_name}, 运行时间为: {execution_time} 秒")
    return data_dict


def generate_data_json(data_queue, request_body, json_obj, ip,start_time, **kwargs):
    data = generate_data_json_request(data_queue, request_body, json_obj, ip_list=[ip],start_time=start_time, **kwargs)
    return data



# finally:
#     # 在离开临界区之前释放锁
#     with lock:
#         global_api_pool.release_ip(ip)
#         current_requests -= 1
#         logger.info(f"!!!!!!!! 当前处理进程数:{current_requests},最大处理数:{MAX_CONCURRENT_REQUESTS}")


if __name__ == "__main__":
    json_str = '''      
{
    "title": "中国平板显示产业重大生产力布局研究",
    "Sections": [
        {
            "index": 1,
            "Section": "第一章 引言",
            "child": [
                {
                    "index": 1,
                    "Section": "第一节 研究背景及意义",
                    "proportion": "1.7%",
                    "data": ""
                },
                {
                    "index": 2,
                    "Section": "第二节 研究目的和内容",
                    "proportion": "1.7%",
                    "data": ""
                },
                {
                    "index": 3,
                    "Section": "第三节 研究方法与数据来源  ",
                    "proportion": "1.7%",
                    "data": ""
                }
            ]
        }
    ]
}
    '''
    import time

    # 记录程序开始时间
    start_time = time.time()

    data_queue = queue.Queue()  # 创
    request_body = {'total_words': 10000}
    json_data = generate_data_json_request(data_queue, request_body, json.loads(json_str),
                                           ip_list=["http://120.133.63.166:8000/v1"])
    print(json.dumps(json_data, ensure_ascii=False))
    # 计算程序运行时间
    execution_time = time.time() - start_time

    print(f"程序运行时间为: {execution_time} 秒")
