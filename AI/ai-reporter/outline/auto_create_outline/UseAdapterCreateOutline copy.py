from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "EMPTY"
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import json
import re
from outline.util.UtilTools import UtilTools
import time
import datetime

class UseAdapterCreateOutline():

    def createOutline(self,subject,words_amount_type,base_url):
        if words_amount_type == 3:
            template = self.create_half_template(subject,words_amount_type,base_url)
        else:
            template = self.create_template(subject,words_amount_type,base_url)
        return self.parse_outline(subject,template)        


    def create_template(self,subject,words_amount_type,base_url):
        now = datetime.datetime.now()
        year = now.year
        chapter_num = 10
        chapter_template = f"""
        你是中文文档编写助手
        当前阶段是用中文编写大纲，你将根据报告主题创建大纲，生成10个章节,每个章节下面有3个小节;大纲只细分到小节,每个小节下面不要再生成内容  
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)
        
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        #{words_amount_type}  
        question = f"""
        你是中文文档编写助手
        当前阶段是用中文编写大纲，你将根据报告主题创建大纲，你的决策将独立执行而不依赖于人类的帮助，请发挥LLM的优势并且追求高效的策略进行输出大纲。
        报告主题: 今年是2024年,报告主题为{subject}
        根据提供的报告主题,生成10个章节,每个章节下面有3个小节;大纲只细分到小节,每个小节下面不要再生成内容  
        """

        prompt = chat_prompt.format_prompt(user_input=question).to_messages()

        try:
            llm = ChatOpenAI(model_name="Baichuan2-13B-Chat", temperature=0.2, frequency_penalty=0,openai_api_base=base_url,request_timeout=300,max_tokens=4096)
            response = llm(prompt, stream=False)
        except Exception as e:
            return str(e), 500
        
        result = response.content
        print(result)
        return result

    def create_half_template(self,subject,words_amount_type,base_url):
        now = datetime.datetime.now()
        year = now.year
        chapter_num = 10
        chapter_template = f"""
        你是中文文档编写助手
        当前阶段是用中文编写大纲，你将根据报告主题创建大纲，生成5个章节,每个章节下面有3个小节;大纲只细分到小节,每个小节下面不要再生成内容  
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)
        
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        #{words_amount_type}  
        question = f"""
        你是中文文档编写助手
        当前阶段是用中文编写大纲，你将根据报告主题创建大纲，你的决策将独立执行而不依赖于人类的帮助，请发挥LLM的优势并且追求高效的策略进行输出大纲。
        报告主题: 今年是2024年,报告主题为{subject}
        根据提供的报告主题,生成5个章节,每个章节下面有3个小节;大纲只细分到小节,每个小节下面不要再生成内容  
        """

        prompt = chat_prompt.format_prompt(user_input=question).to_messages()

        try:
            llm = ChatOpenAI(model_name="Baichuan2-13B-Chat", temperature=0.2, frequency_penalty=0,openai_api_base=base_url,request_timeout=300,max_tokens=4096)
            response = llm(prompt, stream=False)
        except Exception as e:
            return str(e), 500
        
        result = response.content
        print(result)
        return result


    def parse_outline(self,subject,template):
        tools = UtilTools()
        zhang = 0
        dagang = {"title":"","Sections":[]}
        ispass = False
        zhang_list = []
        dagang["title"] = subject
        bar_num = 0
        print(template)
        lines = template.split("\n")
        jie = 0
        tag = True
        for line in lines:
            sub_line = line.strip()
            if sub_line == "":
                continue
            if re.match("^[一二三四五六七八九十]",sub_line) :
                tag = False
                if "、" in sub_line:
                    paragraphs = sub_line.split("、")
                if "." in sub_line:
                    paragraphs = sub_line.split(".")
                print(paragraphs)
                zhang = zhang + 1
                jie = 0
                zhang_num = tools.digit_to_chinese(zhang)
                if "一十" in zhang_num:
                    zhang_num = zhang_num.replace("一十","十")
                zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraphs[1],"child":[]}
                dagang["Sections"].append(zhang_section)
            
            
            if tag:
                if re.match("^[\d]",sub_line) and not re.match("^[\d]+(.[\d])",sub_line):
                    paragraphs = sub_line.split(". ")
                    print(paragraphs)
                    zhang = zhang + 1
                    jie = 0
                    zhang_num = tools.digit_to_chinese(zhang)
                    if "一十" in zhang_num:
                        zhang_num = zhang_num.replace("一十","十")
                    zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraphs[1],"child":[]}
                    dagang["Sections"].append(zhang_section)
                if sub_line.startswith("章节"):
                    if "：" in sub_line:
                        paragraphs = sub_line.split("：")
                    if ":" in sub_line:
                        paragraphs = sub_line.split(": ")
                    print(paragraphs)
                    zhang = zhang + 1
                    jie = 0
                    zhang_num = tools.digit_to_chinese(zhang)
                    if "一十" in zhang_num:
                        zhang_num = zhang_num.replace("一十","十")
                    zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraphs[1],"child":[]}
                    dagang["Sections"].append(zhang_section)
                if re.match("^(第)[\u4e00-\u9fa5]+(章)",sub_line) or re.match("^(第)[0-9]+(章)",sub_line):
                    if "：" in sub_line:
                        paragraphs = sub_line.split("：")
                    if ":" in sub_line:
                        paragraphs = sub_line.split(": ")
                    print(paragraphs)
                    zhang = zhang + 1
                    jie = 0
                    zhang_num = tools.digit_to_chinese(zhang)
                    if "一十" in zhang_num:
                        zhang_num = zhang_num.replace("一十","十")
                    zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraphs[1],"child":[]}
                    dagang["Sections"].append(zhang_section)

                
                
                if  re.match("^[\d]+(.[\d])",sub_line) or re.match("^[a-z](.)",sub_line) or re.match("^[A-Z](.)",sub_line):
                    sub_line = sub_line.replace("小节: ","")
                    sub_line = sub_line.replace("小节：","")
                    paragraphs = sub_line.split(" ")
                    print(paragraphs)
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    jie_content = ""
                    if len(paragraphs) == 1:
                        jie_content = re.sub("[\d]+(.[\d])", "", paragraphs[0])
                        jie_content = re.sub("[a-z](.)", "", jie_content)
                        jie_content = re.sub("[A-Z](.)", "", jie_content)
                    else:
                        jie_content = paragraphs[1]
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  jie_content}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num = bar_num + 1

                if sub_line.startswith("小节"):
                    if "：" in sub_line:
                        paragraphs = sub_line.split("：")
                    if ":" in sub_line:
                        paragraphs = sub_line.split(": ")
                    print(paragraphs)
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  paragraphs[1]}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num = bar_num + 1

                if re.match("^(第)[\u4e00-\u9fa5]+(节)$",sub_line) or re.match("^(第)[0-9]+(节)$",sub_line) :
                    if "：" in sub_line:
                        paragraphs = sub_line.split("：")
                    if ":" in sub_line:
                        paragraphs = sub_line.split(": ")
                    print(paragraphs)
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  paragraphs[1]}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num += 1
            else:
                if re.match("^[\d]",sub_line) or re.match("^[\d]+(.[\d])",sub_line):
                    if ". " in sub_line:
                        paragraphs = sub_line.split(". ")
                    else:
                        paragraphs = sub_line.split(" ")
                    print(paragraphs)
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    jie_content = ""
                    if len(paragraphs) == 1:
                        jie_content = re.sub("^[\d]+(.[\d])", "", paragraphs[0])
                    else:
                        jie_content = paragraphs[1]
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  jie_content}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num += 1

        avg = str(round(round(1 / bar_num, 3) * 100,1)) + "%"
        for i in range(len(dagang["Sections"])):
            for j in range(len(dagang["Sections"][i]["child"])):
                dagang["Sections"][i]["child"][j]["proportion"] = avg
                dagang["Sections"][i]["child"][j]["data"] = ""    

        print(json.dumps(dagang,indent=4, ensure_ascii=False))
        return dagang,bar_num

        
           



