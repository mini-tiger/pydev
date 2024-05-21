from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "EMPTY"
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import json
import re
from outline.util.UtilTools import UtilTools
import time
import datetime
current_directory = os.path.dirname(__file__)
class UseAdapterCreateOutline():

    def createOutline(self,subject,words_amount_type,base_url):

        if words_amount_type == 3:
            template = self.create_half_template(subject,words_amount_type,base_url)
        else:
            template = self.create_template(subject,words_amount_type,base_url)

 
        template_json = self.convert_json(subject,template,base_url)   

        return self.parse_outline(subject,template_json,base_url,template)   




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
            llm = ChatOpenAI(model_name="Baichuan2-13B-Chat", temperature=0.2, frequency_penalty=0,openai_api_base=base_url,request_timeout=300,max_tokens=8192)
            response = llm(prompt, stream=False)
        except Exception as e:
            return str(e), 500
        
        result = response.content
        print(result)
        return result


    def convert_json(self,subject,template,base_url):
        chapter_template = f"""
        你是中文大纲目录整理助手
        你可以根据大纲目录内容，整理成json格式
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)
        
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        #{words_amount_type}  
        question = f"""
        你是中文大纲目录整理助手
        大纲内容如下
        {template}  
        ------------
        请把上面的大纲内容，整理成json格式 {{"items":["title": "章节名称","subitems": [{{ "title":"小节名称" }}]}}
        """

        prompt = chat_prompt.format_prompt(user_input=question).to_messages()
        try:
            llm = ChatOpenAI(model_name="Baichuan2-13B-Chat", temperature=0.2, frequency_penalty=0,openai_api_base=base_url,request_timeout=300,max_tokens=4096)
            response = llm(prompt, stream=False)
            result = json.loads(response.content)
        except Exception as e:
            return None
        print(result)
        return result


    def parse_outline(self,subject,template_json,base_url,template):
        
        outline = {"title":"","Sections":[]}
        outline["title"] = subject
        bar_num = 0
        if template_json == None:
            print("------------01---------------")
            outline,bar_num = self.parse_line_content(subject,template)
            if outline == None or bar_num == 0:
                print("------------02---------------")
                outline,bar_num = self.parse_subject_model(subject,base_url)

        else:
            outline,bar_num = self.parse_json_content(subject,template_json)
            print("------------03---------------")
            if outline == None or bar_num == 0:
                print("------------04---------------")
                outline,bar_num = self.parse_line_content(subject,template)
                if outline == None or bar_num == 0:
                    print("------------05---------------")
                    outline,bar_num = self.parse_subject_model(subject,base_url)
 
        avg = str(round(round(1 / bar_num, 3) * 100,1)) + "%"
        for i in range(len(outline["Sections"])):
            for j in range(len(outline["Sections"][i]["child"])):
                outline["Sections"][i]["child"][j]["proportion"] = avg
                outline["Sections"][i]["child"][j]["data"] = ""
        print(outline)
        return outline,bar_num

    def parse_line_content(self,subject,template):
        
        outline = {"title":"","Sections":[]}
        outline["title"] = subject
        tools = UtilTools()
        bar_num = 0
        try:
            pre_paragraphs = template.split("\n")
            paragraphs = []
            for original_paragraph in pre_paragraphs:
                original_paragraph = original_paragraph.strip()
                original_paragraph = original_paragraph.replace("#","")
                if re.match("^[一二三四五六七八九十]",original_paragraph) :
                    paragraphs.append(original_paragraph)
                elif re.match("^[\d]",original_paragraph) and not re.match("^[\d]+(.[\d])",original_paragraph):
                    paragraphs.append(original_paragraph)
                elif original_paragraph.startswith("章节"):
                    paragraphs.append(original_paragraph)
                elif re.match("^(第)[\u4e00-\u9fa5]+(章)",original_paragraph) or re.match("^(第)[0-9]+(章)",original_paragraph):
                    paragraphs.append(original_paragraph)
                elif re.match("^[\d]+(.[\d])",original_paragraph) or re.match("^[a-z](.)",original_paragraph) or re.match("^[A-Z](.)",original_paragraph):
                    paragraphs.append(original_paragraph)
                elif original_paragraph.startswith("小节"):
                    paragraphs.append(original_paragraph)
                elif re.match("^(第)[\u4e00-\u9fa5]+(节)$",original_paragraph) or re.match("^(第)[0-9]+(节)$",original_paragraph) :
                    paragraphs.append(original_paragraph)
                elif re.match("^[\d]",original_paragraph) or re.match("^[\d]+(.[\d])",original_paragraph):
                    paragraphs.append(original_paragraph)
            zhang = 0
            jie = 0
            for index,content in enumerate(paragraphs):

                if index % 4 == 0:
                    paragraph = content
                    print(paragraph)
                    paragraph = re.sub("(第)[\u4e00-\u9fa5]+(章)","",paragraph)
                    paragraph = re.sub("(第)[\u4e00-\u9fa5]+(节)","",paragraph)
                    paragraph = re.sub("章节","",paragraph)
                    paragraph = re.sub("小节","",paragraph)
                    paragraph = re.sub("：","",paragraph)
                    paragraph = re.sub(":","",paragraph)
                    paragraph = re.sub("[\d]+(.[\d])", "", paragraph)
                    paragraph = re.sub("[\d]", "", paragraph)
                    paragraph = re.sub("[a-z](.)", "", paragraph)
                    paragraph = re.sub("[A-Z](.)", "", paragraph)
                    zhang = zhang + 1
                    jie = 0
                    zhang_num = tools.digit_to_chinese(zhang)
                    if "一十" in zhang_num:
                        zhang_num = zhang_num.replace("一十","十")
                    zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraph,"child":[]}
                    outline["Sections"].append(zhang_section)
                else:
                    paragraph = content
                    paragraph = re.sub("(第)[\u4e00-\u9fa5]+(章)","",paragraph)
                    paragraph = re.sub("(第)[\u4e00-\u9fa5]+(节)","",paragraph)
                    paragraph = re.sub("章节","",paragraph)
                    paragraph = re.sub("小节","",paragraph)
                    paragraph = re.sub("：","",paragraph)
                    paragraph = re.sub(":","",paragraph)
                    paragraph = re.sub("[\d]+(.[\d])", "", paragraph)
                    paragraph = re.sub("[\d]", "", paragraph)
                    paragraph = re.sub("[a-z](.)", "", paragraph)
                    paragraph = re.sub("[A-Z](.)", "", paragraph)
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  paragraph}
                    outline["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num = bar_num + 1
        except Exception as e:
            return None,0
        return outline,bar_num

    
    def parse_json_content(self,subject,template_json):
        outline = {"title":"","Sections":[]}
        outline["title"] = subject
        tools = UtilTools()
        bar_num = 0
        try:
            for item_index,item in enumerate(template_json["items"]):
                chapter_title = item["title"]
                paragraph = re.sub("(第)[\u4e00-\u9fa5]+(章)","",chapter_title)
                paragraph = re.sub("(第)[\u4e00-\u9fa5]+(节)","",paragraph)
                paragraph = re.sub("章节","",paragraph)
                paragraph = re.sub("小节","",paragraph)
                paragraph = re.sub("：","",paragraph)
                paragraph = re.sub(":","",paragraph)
                paragraph = re.sub("[\d]+(.[\d])", "", paragraph)
                paragraph = re.sub("[\d]", "", paragraph)
                paragraph = re.sub("[a-z](.)", "", paragraph)
                paragraph = re.sub("[A-Z](.)", "", paragraph)
                paragraph = paragraph.replace("#","")
                zhang_num = tools.digit_to_chinese(item_index+1)
                if "一十" in zhang_num:
                    zhang_num = zhang_num.replace("一十","十")
                zhang_section = {"index": item_index,"Section": "第" + zhang_num + "章 " +  paragraph,"child":[]}
                outline["Sections"].append(zhang_section)
                for subitem_index,subitem in enumerate(item["subitems"]):
                    bar_title = subitem["title"]
                    paragraph = re.sub("(第)[\u4e00-\u9fa5]+(章)","",bar_title)
                    paragraph = re.sub("(第)[\u4e00-\u9fa5]+(节)","",paragraph)
                    paragraph = re.sub("章节","",paragraph)
                    paragraph = re.sub("小节","",paragraph)
                    paragraph = re.sub("：","",paragraph)
                    paragraph = re.sub(":","",paragraph)
                    paragraph = re.sub("[\d]+(.[\d])", "", paragraph)
                    paragraph = re.sub("[\d]", "", paragraph)
                    paragraph = re.sub("[a-z](.)", "", paragraph)
                    paragraph = re.sub("[A-Z](.)", "", paragraph)
                    paragraph = paragraph.replace("#","")
                    jie_num = tools.digit_to_chinese(subitem_index + 1)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": subitem_index,"Section": "第" + jie_num + "节 " +  paragraph}
                    outline["Sections"][item_index]["child"].append(jie_section)
                    bar_num = bar_num + 1
        except Exception as e:
            return None,0
        return outline,bar_num

    def parse_subject_model(self,subject,base_url):
        chapter_template = f"""
        你是一个报告提取信息助手，你可以从报告、研究报告、白皮书，合同，论文，研究论文的题目抽取主题获取关键字，关键字是题目本质的词汇或短语
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)
        
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        #{words_amount_type}  
        question = f"""
        你是从题目抽取主题获取关键字的助手，关键字是题目本质核心的词汇或短语
        题目如下：
        {subject}  
        ------------
        请从上面的题目中，抽取最核心的一个关键字,并整理成json格式 {{"keyword":"关键字"}}
        """

        prompt = chat_prompt.format_prompt(user_input=question).to_messages()
        keyword_answer = ""
        keyword_json = {}
        keyword = ""
        try:
            llm = ChatOpenAI(model_name="Baichuan2-13B-Chat", temperature=0.2, frequency_penalty=0,openai_api_base=base_url,request_timeout=300,max_tokens=4096)
            response = llm(prompt, stream=False)
            keyword_answer = response.content
        except Exception as e:
            keyword_answer = ""
        try:
            keyword_json = json.loads(keyword_answer)
            keyword = keyword_json["keyword"]
        except Exception as e:
            keyword = keyword_answer
        
        outline = {"title":"","Sections":[]}
        outline["title"] = subject
        bar_num = 0
        model_json_file = "common_model.json"
        model_json_path = os.path.join(current_directory,"common_model", model_json_file)
        with open(model_json_path, 'r', encoding='utf-8') as f:
            outline = json.load(f)
        
        outline["title"] = subject
        for i in range(len(outline["Sections"])):
            chapter = outline["Sections"][i]["Section"]
            chapter = re.sub("\\{keyword\\}",keyword,chapter)
            outline["Sections"][i]["Section"] = chapter
            for j in range(len(outline["Sections"][i]["child"])):
                bar = outline["Sections"][i]["child"][j]["Section"]
                bar = re.sub("\\{keyword\\}",keyword,bar)
                outline["Sections"][i]["child"][j]["Section"] = bar
                bar_num += 1
        return outline,bar_num

        
           



