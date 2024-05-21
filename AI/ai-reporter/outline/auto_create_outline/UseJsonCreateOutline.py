from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "EMPTY"
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import json
from outline.util.UtilTools import UtilTools
import time
import datetime
import xml.etree.ElementTree as ET


class UseJsonCreateOutline():

    def createOutline(self,subject,words_amount_type,base_url):
        template = self.create_template(subject,words_amount_type,base_url)
        print(template)
        return self.parseAndCreateXml(subject,template)


    def create_template(self,subject,words_amount_type,base_url):
        now = datetime.datetime.now()
        year = now.year
        chapter_num = words_amount_type * 2
        chapter_template = f"""
        你是文档和报告的编写助手
        当前阶段是大纲编写，你将根据报告主题创建大纲，你的决策将独立执行而不依赖于人类的帮助，
        请发挥LLM的优势并且追求高效的策略进行输出大纲。
        报告主题: 今年是{year}年,根据提供的报告主题,生成{chapter_num}个章节,每个章节至少有3个小节;大纲只细分到小节,每个小节下面不要再生成内容;
        大纲中第一章为引言;
        大纲章节中不能包含的章节有：附录、致谢、空白页、封底、版权页、参考文献。
        你只能以以下xml列表的格式生成大纲
        <chapters>
            <chapter>
                <chapter_title>章节10标题</chapter_title>
                <sections>
                    <section_title>小节1标题</section_title>
                    <section_title>小节2标题</section_title>
                    <section_title>小节3标题</section_title>
                </sections>
            </chapter>
        </chaters>        
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)
        
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        #{words_amount_type}  
        question = f"""
        你是文档和报告的编写助手
        当前阶段是大纲编写，你将根据报告主题创建大纲，你的决策将独立执行而不依赖于人类的帮助，
        请发挥LLM的优势并且追求高效的策略进行输出大纲。
        报告主题: 今年是{year}年,报告主题为{subject}
        根据提供的报告主题,生成{chapter_num}个章节,每个章节有3个小节;
        大纲第一章为引言;
        大纲章节中不能包含的章节有：附录、致谢、空白页、封底、版权页、参考文献。
        你只能以以下xml列表的格式生成大纲
        <chapters>
            <chapter>
                <chapter_title>章节标题</chapter_title>
                <chapter_index>1</chapter_index>
                <sections>
                    <section_title>小节标题</section_title>
                    <section_title>小节标题</section_title>
                    <section_title>小节标题</section_title>
                </sections>
            </chapter>
        </chaters>        
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


    def merge_outline(firstemplate,endtemplate):
        merge_data = []
        firstdata = json.loads(firstemplate)
        enddata = json.loads(endtemplate)
        merge_data = [obj for obj in (firstdata + enddata)]
        return merge_data

    def parseAndCreateXml(self,subject,data):
        chapter_names = []
        tools = UtilTools()
        bar_num = 0
        #data = json.loads(jsonStr)
        dagang = {"title":"","Sections":[]}
        dagang["title"] = subject
        chapters = []
        zhang = 0
        print(data)
        root = ET.fromstring(data)
        for chapter in root.findall("chapter"):

            chapter_title = chapter.find('chapter_title').text
            zhang += 1
            zhang_num = tools.digit_to_chinese(zhang)
            if "一十" in zhang_num:
                zhang_num = zhang_num.replace("一十","十")
            zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  chapter_title,"child":[]}
            dagang["Sections"].append(zhang_section)
            jie = 1
            for section in chapter.findall('sections/section_title'):
                jie_num = tools.digit_to_chinese(jie)
                section_title = section.text
                jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  section_title}
                dagang["Sections"][zhang-1]["child"].append(jie_section)
                bar_num += 1
                jie += 1


        avg = str(round(round(1 / bar_num, 3) * 100,1)) + "%"
        for i in range(len(dagang["Sections"])):
            for j in range(len(dagang["Sections"][i]["child"])):
                dagang["Sections"][i]["child"][j]["proportion"] = avg
                dagang["Sections"][i]["child"][j]["data"] = ""
        return dagang,bar_num
            
 


    def parseAndCreateJson(self,subject,data):
        chapter_names = []
        tools = UtilTools()
        bar_num = 0
        #data = json.loads(jsonStr)
        dagang = {"title":"","Sections":[]}
        dagang["title"] = subject
        chapters = []
        for index,obj in enumerate(data):
            chapter_name = obj["ct"]
            if chapter_name in chapter_names:
                continue
            chapter_names.append(chapter_name)
            zhang = index+1
            zhang_num = tools.digit_to_chinese(zhang)
            if "一十" in zhang_num:
                zhang_num = zhang_num.replace("一十","十")
            chapter_obj = {"index": zhang,"Section": "第" + zhang_num + "章 " +  chapter_name,"child":[]}
            
            for jndex,jbj in enumerate(obj["Section"]):
                jie = jndex + 1
                jie_num = tools.digit_to_chinese(jie)
                bar_obj = {"index": jie,"Section": "第" + jie_num + "节 " +  obj["st"]}
                chapter_obj.append(bar_obj)
                bar_num += 1
            chapters.append(chapter_obj)


        avg = str(round(round(1 / bar_num, 3) * 100,1)) + "%"
        for i in range(len(dagang["Sections"])):
            for j in range(len(dagang["Sections"][i]["child"])):
                dagang["Sections"][i]["child"][j]["proportion"] = avg
                dagang["Sections"][i]["child"][j]["data"] = ""
        return dagang,bar_num

        
                




