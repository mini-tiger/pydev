from distutils.command import config
from tempfile import NamedTemporaryFile
import re
import os
import json
import jieba.analyse
import requests
# 创建聊天模型
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
import openai
from langchain import PromptTemplate
from outline.config import parsers
from outline.auto_create_outline.AutoCreateOutline import AutoCreateOutline
from outline.auto_create_outline.UseJsonCreateOutline import UseJsonCreateOutline
from outline.auto_create_outline.UseAdapterCreateOutline import UseAdapterCreateOutline

from webapi.log.setup import logger
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

os.environ["OPENAI_API_KEY"] = 'EMPTY'
argparse = parsers()
#llm = ChatOpenAI(model_name="qwen1.5", temperature=0, openai_api_base=argparse.yi_model_url)

current_directory = os.path.dirname(__file__)

area_list = []
area_list_path = os.path.join(current_directory+"/data/", "area_list.json")
with open(area_list_path, 'r', encoding='utf-8') as f:
    area_list = json.load(f)

report_type = {}
report_type_path = os.path.join(current_directory+"/data/", "report_type.json")
with open(report_type_path, 'r', encoding='utf-8') as f:
    report_type = json.load(f)

type_model = {}
type_model_path = os.path.join(current_directory+"/data/", "type_model.json")
with open(type_model_path, 'r', encoding='utf-8') as f:
    type_model = json.load(f)

words_amount_type = {}
words_amount_path = os.path.join(current_directory+"/data/", "words_amount.json")
with open(words_amount_path, 'r', encoding='utf-8') as f:
    words_amount_type = json.load(f)

create_outline_model = {}
create_outline_model_path = os.path.join(current_directory+"/data/", "create_outline_model.json")
with open(create_outline_model_path, 'r', encoding='utf-8') as f:
    create_outline_model = json.load(f)


def getAnswer(text):
    args = parsers()
    openai.api_key = "Empty"
    openai.base_url = args.qwen_model_url
    completion = openai.chat.completions.create(
        model="ChatModel",
        messages=[
            {"role": "user", "content": text},
        ],
        max_tokens=4000, 
        n=1,  # 设置生成的选项数量为1
        stop=None,  # 不设置停止条件
        temperature=0,  # 设置温度为0.5，
        timeout=300,
    )
    content = completion.choices[0].message.content
    return content


class CreateOutline():

    #获取所有报告的类型
    def getReportType(self):
        keys = []
        outlineModelName = {}
        for key, value in report_type.items():
            keys.append(key)
            name = report_type[key]
            model_name = name + ".docx"
            outlineModelName[key] = model_name
        return keys,outlineModelName


    #查询报告的行业类型
    def checkReportType(self,subject):
        args = parsers()
        post_data = {
            'subject': subject
        }
        url = args.bert_classify_model_url
        response = requests.post(url, data=json.dumps(post_data))
        print(response.text)
        return response.text

    #判断是否需要填写关键字
    def checkKeyWord(self,subject):
        
        template =  """{subject}是写什么东西(物体)，只回答具体东西的名称。"""
        prompt = PromptTemplate(
            input_variables=["subject"],
            template=template,
        )
        
        prompt_text = prompt.format(subject=subject)
        keyword = getAnswer(prompt_text)
        
        if keyword == "报告":
            return self.checkAgainKeyWord(subject,1)
        elif keyword in subject:
            return {"code":200,"isNeedKeyWord":False,"keyword":keyword}
        else:
            return self.checkAgainKeyWord(subject,1)
    
    #多次判断填写关键字
    def checkAgainKeyWord(self,subject,count):
        if count > 4:
            return {"code":200,"isNeedKeyWord":True}
        count += 1
        template =  """{subject}是写什么东西(物体)，只回答具体东西的名称。"""
        prompt = PromptTemplate(
            input_variables=["subject"],
            template=template,
        )
        prompt_text = prompt.format(subject=subject)
        keyword = getAnswer(prompt_text)
        print(keyword)
        if keyword == "报告":
            return self.checkAgainKeyWord(subject,count)
        elif keyword in subject:
            return {"code":200,"isNeedKeyWord":False,"keyword":keyword}
        else:
            return self.checkAgainKeyWord(subject,count)


    #生成大纲
    def create_outline(self,subject,keyword,type,words_amount,base_url):
        args = parsers()
        jieba.load_userdict(area_list)
        words = jieba.cut(subject, cut_all=False)
        area = ""
        for word in words:
            if word in area_list:
                area = word
        r_type = report_type[type]
        outline = {}
        if r_type == args.intelligent_generation:
            wat = words_amount_type[str(words_amount)]
            if create_outline_model[args.create_outline_model] == 'inner_model':
                auto = AutoCreateOutline()
                data,bar_num = auto.createOutline(subject,wat,base_url)
            elif create_outline_model[args.create_outline_model] == 'outer_model':
                auto = UseJsonCreateOutline()
                data,bar_num = auto.createOutline(subject,wat,base_url)
            elif create_outline_model[args.create_outline_model] == 'adapter_model':
                auto = UseAdapterCreateOutline()
                data,bar_num = auto.createOutline(subject,wat,base_url)
            else:
                auto = AutoCreateOutline()
                data,bar_num = auto.createOutline(subject,wat,base_url)
            outline = json.dumps(data, indent=4, ensure_ascii=False)
        else:
            model_json_file = type_model[r_type]
            model_json_path = os.path.join(current_directory+"/model_json/", model_json_file)
            with open(model_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            title = re.sub("\\{title\\}",data["title"],subject)
            data["title"] = title
            bar_num = 0
            for i in range(len(data["Sections"])):
                chapter = data["Sections"][i]["Section"]
                chapter = re.sub("\\{keyword\\}",keyword,chapter)
                chapter = re.sub("\\{area\\}",area,chapter)
                data["Sections"][i]["Section"] = chapter
                for j in range(len(data["Sections"][i]["child"])):
                    bar = data["Sections"][i]["child"][j]["Section"]
                    bar = re.sub("\\{keyword\\}",keyword,bar)
                    bar = re.sub("\\{area\\}",area,bar)
                    data["Sections"][i]["child"][j]["Section"] = bar
                    data["Sections"][i]["child"][j]["data"] = ""
                    bar_num += 1

            avg = str(round(round(1 / bar_num, 3) * 100,1)) + "%"
            for i in range(len(data["Sections"])):
                for j in range(len(data["Sections"][i]["child"])):
                    data["Sections"][i]["child"][j]["proportion"] = avg

            outline = json.dumps(data, indent=4, ensure_ascii=False)
        
        #print(outline)
        return {"code":200,"outline":outline,"bar_num":bar_num}

def getOutlineModelName(self,type):
    name = report_type[type]
    model_name = name + ".docx"
    return model_name
        

# c = CreateOutline()
# #c.create_outline("中国自行车发的展行业研究报告","自行车","车辆")
# c.checkKeyWord("中国美的电饭锅产业研究报告")
# #c.getReportType()
# c.checkReportType("中国美的电饭锅产业研究报告")