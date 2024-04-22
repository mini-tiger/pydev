from langchain.chat_models import ChatOpenAI
import openai
import os
os.environ["OPENAI_API_KEY"] = 'EMPTY'
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import datetime
from outline.config import parsers
from outline.auto_create_outline.AutoParse import AutoParse
from webapi.log.setup import logger
from outline.config import parsers
from outline.util.UtilTools import UtilTools
import time

args = parsers()
# http://120.133.83.145:8000/v1/

#llm = ChatOpenAI(model_name="ChatModel", temperature=0, openai_api_base="http://120.133.83.145:8000/v1/")

#大纲章节中不包含的章节有：未来展望、结论与建议、附录、致谢、空白页、封底、版权页、参考文献、致谢。

class AutoCreateOutline():

    def createOutline(self,subject,words_amount_type,base_url):
        ap = AutoParse()
        args = parsers()
        execute_count = args.execute_count
        #create_chapter_count = args.create_chapter_count
        create_chapter_count = words_amount_type
        result_list = []
        result_list = self.xunhuanMakeOutline(subject,result_list,execute_count,execute_count,create_chapter_count,base_url)
        chatpter_list,bar_num = ap.parse2Json(subject,result_list,execute_count*create_chapter_count)
        return chatpter_list,bar_num

    def xunhuanMakeOutline(self,subject,result_list,index,sum_num,create_chapter_count,base_url):
        #每次生成10章
        prompt = ""
        if result_list == None:
            result_list = []
            prompt = self.first_template(subject,(sum_num-index),create_chapter_count)
            #logger.info(f"prompt-----------------------\n{prompt}")
            print("first_template")
        elif index == 1:
            content = ""
            for p in result_list:
                content = content + "\n" + p
            prompt = self.end_temple(subject,content,(sum_num-index),create_chapter_count)
            #logger.info(f"prompt-----------------------\n{prompt}")
            print("end_temple")
        else:    
            content = ""
            for p in result_list:
                content = content + "\n" + p
            prompt = self.subsequent_temple(subject,content,(sum_num-index),create_chapter_count)
            #logger.info(f"prompt-----------------------\n{prompt}")
            print("subsequent_temple")
        start_time = time.time()
        try:
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2, frequency_penalty=0,openai_api_base=base_url,request_timeout=300)
            response = llm(prompt, stream=False)
        except Exception as e:
            return str(e), 500
        end_time = time.time()
        text = response.content
        execution_time = end_time - start_time
        logger.info(f"应用时间为{execution_time}")
        logger.info(f'生成的目录为：-------------------------------------------\n{text}')
        result_list.append(text)
        print(text)
        index -= 1
        print("index====="+str(index))
        if index >=1:
            #result_list = xunhuanMakeOutline(subject,result_list,index)
            return self.xunhuanMakeOutline(subject,result_list,index,sum_num,create_chapter_count,base_url)
        else:
            return result_list
        return result_list

    def first_template(self,subject,chapter_num,create_chapter_count):
        args = parsers()
        tools = UtilTools()
        #create_chapter_count = args.create_chapter_count
        chapter_begin = chapter_num * create_chapter_count + 1
        chapter_end = (chapter_num + 1) * create_chapter_count
        now = datetime.datetime.now()
        year = now.year
        chapter_begin = tools.digit_to_chinese(chapter_begin)
        chapter_end = tools.digit_to_chinese(chapter_end)
        chapter_template = f"""
        根据示例回答问题
        －－－－－－－
        示例:
        Human: 参考以下文本回答问题：
        －－－－－－－
        文本:
        今年是{year}年,企业需要编写研究报告，根据提供的报告主题生成目录，目录中每一章至少有3个小节，包含第一章节为引言;
        大纲只细分到小节,每个小节下面不要再生成内容。目录中生成的章节内容不可以重复，按照章节顺序生成目录
        
        －－－－－－－
        问题:
        今年是2024年,报告主题为中国互联网近20年发展状况及未来趋势研究报告，请编写前{chapter_end}个章节的大纲并含有包含引言;
        大纲只细分到小节,每个小节下面不要再生成内容。目录中生成的章节内容不可以重复，按照章节顺序生成目录

        －－－－－－－
        返回固定格式:
        第三章 中国互联网行业结构与规模
            第一节 研究背景及意义
            第二节 研究目的和内容
            第三节 研究方法与数据来源
        －－－－－－－
        AI:
        第二章 中国互联网发展历程
            第一节 1990年代互联网发展概况
            第二节 2000-2007年中国互联网发展阶段
            第三节 2008-2012年中国互联网发展阶段
            第四节 2013年以来中国互联网发展现状
        
        －－－－－－－
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)

        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])

        question = f'''
        参考以下文本回答问题：
        －－－－－－－
        文本:
        今年是{year}年,企业需要编写研究报告，根据提供的报告主题生成目录，目录中每个章节至少有3个小节,包含引言,大纲只细分到小节,每个小节下面不要再生成内容。
        大纲只细分到小节,每个小节下面不要再生成内容。目录中生成的章节内容不可以重复，
        按照章节顺序从第{chapter_begin}到第{chapter_end}章节生成目录,第一章为引言,每个章节都要有换行符\n
        －－－－－－－
        问题:
        今年是{year}年,报告主题为{subject}生成目录，目录中每个章节至少有3个小节,请编写从第{chapter_begin}到第{chapter_end}章节的大纲并含有包含引言,大纲只细分到小节,每个小节下面不要再生成内容。
        大纲只细分到小节,每个小节下面不要再生成内容。
        目录中生成的章节内容不可以重复，按照章节顺序从第{chapter_begin}到第{chapter_end}章节生成目录,第一章为引言,每个章节都要有换行符\n
        －－－－－－－
        返回固定格式样例
        第一章 引言
            第一节 研究背景及意义
            第二节 研究目的和内容
            第三节 研究方法与数据来源

        总结格式为第N章 xxxxx  \n 第N节 \n
        '''

        prompt = chat_prompt.format_prompt(user_input=question).to_messages()
        print(prompt)
        return prompt

    def subsequent_temple(self,subject,content,chapter_num,create_chapter_count):
        now = datetime.datetime.now()
        year = now.year
        args = parsers()
        tools = UtilTools()
        #create_chapter_count = args.create_chapter_count
        have_chapter_begin = chapter_num * create_chapter_count
        chapter_begin = chapter_num * create_chapter_count + 1
        chapter_end = (chapter_num + 1) * create_chapter_count
        chapter_begin = tools.digit_to_chinese(chapter_begin)
        chapter_end = tools.digit_to_chinese(chapter_end)
        chapter_template = f"""
        根据示例回答问题
        －－－－－－－
        示例:
        Human: 参考以下文本回答问题：
        －－－－－－－
        文本:
        今年是{year}年,企业需要编写研究报告,根据提供的报告主题,每个章节至少有3个小节,其中包含引言;
        大纲只细分到小节,每个小节下面不要再生成内容;
        按照顺序生成章节
        －－－－－－－
        问题:
        今年是{year}年,报告主题为中国互联网近20年发展状况及未来趋势研究报告，
        已知已有{have_chapter_begin}个章节大刚，每章标题前要有第N章，每个小节前有第N节;
        大纲只细分到小节,每个小节下面不要再生成内容，生成的章节不能重复,按照顺序生成
        －－－－－－－
        请继续编写后面的10个章节大纲，每章标题前要有第N章,每个小节前有第N节,其中包含引言;
        大纲只细分到小节,每个小节下面不要再生成内容;
        －－－－－－－
        返回固定格式样例
        第三章 中国互联网行业结构与规模
            第一节 互联网行业分类及特点
            第二节 2019年中国互联网行业规模与结构数据
            第三节 2020年中国互联网行业发展趋势
        －－－－－－－
        AI:
        第四章 引言
            第一节 研究背景及意义
            第二节 研究目的和内容
            第三节 研究方法与数据来源

        
        －－－－－－－
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        # 用户的询问
        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)

        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        question = f'''参考以下文本回答问题：
        －－－－－－－
        文本:
        今年是{year}年,企业需要编写研究报告,根据提供的报告主题,每个章节至少有3个小节;
        大纲只细分到小节,每个小节下面不要再生成内容;
        按照顺序生成从第{chapter_begin}到第{chapter_end}章节,每个章节都要有换行符\n
        －－－－－－－
        问题:
        今年是{year}年,报告主题为中{subject}，
        
        大纲只细分到小节,每个小节下面不要再生成内容;
        大纲章节中不包含的章节有：未来展望、结论与建议、附录、致谢、空白页、封底、版权页、参考文献、致谢。
        按照顺序生成从第{chapter_begin}到第{chapter_end}章节,每个章节都要有换行符\n
        已知已生成了以下{have_chapter_begin}个章节大刚,目录大纲如下
        {content}
        －－－－－－－
        请继续编写从第{chapter_begin}到第{chapter_end}章节大纲;
        大纲只细分到小节,每个小节下面不要再生成内容;
        按照顺序生成从第{chapter_begin}到第{chapter_end}章节,每个章节都要有换行符\n
        －－－－－－－
        返回固定格式样例 
        第一章 引言
            第一节 研究背景及意义
            第二节 研究目的和内容
            第三节 研究方法与数据来源
        
        总结格式为第N章 xxxxx  \n 第N节 \n
        '''
        prompt = chat_prompt.format_prompt(user_input=question).to_messages()
        return prompt

    def end_temple(self,subject,content,chapter_num,create_chapter_count):
        now = datetime.datetime.now()
        year = now.year
        args = parsers()
        #create_chapter_count = args.create_chapter_count
        have_chapter_begin = chapter_num * create_chapter_count
        chapter_begin = chapter_num * create_chapter_count + 1
        chapter_end = (chapter_num + 1) * create_chapter_count
        tools = UtilTools()
        chapter_begin = tools.digit_to_chinese(chapter_begin)
        chapter_end = tools.digit_to_chinese(chapter_end)
        chapter_template = f"""
        根据示例回答问题
        －－－－－－－
        示例:
        Human: 参考以下文本回答问题：
        －－－－－－－
        文本:
        今年是{year}年,企业需要编写研究报告,根据提供的报告主题,每个章节至少有3个小节,其中包含引言;
        大纲只细分到小节,每个小节下面不要再生成内容;
        大纲章节中不包含的章节有：引言、附录、致谢、空白页、封底、版权页、参考文献、致谢。
        按照顺序生成章节
        －－－－－－－
        问题:
        今年是{year}年,报告主题为中国互联网近20年发展状况及未来趋势研究报告，
        已知已有{have_chapter_begin}个章节大刚，每章标题前要有第N章，每个小节前有第N节;大纲只细分到小节,每个小节下面不要再生成内容，生成的章节不能重复,按照顺序生成
        －－－－－－－
        请继续编写后面的{chapter_end}个章节大纲，每章标题前要有第N章,每个小节前有第N节,其中包含引言;大纲只细分到小节,每个小节下面不要再生成内容;
        －－－－－－－
        返回固定格式样例
        第三章 中国互联网行业结构与规模
            第一节 互联网行业分类及特点
            第二节 2019年中国互联网行业规模与结构数据
            第三节 2020年中国互联网行业发展趋势
        －－－－－－－
        AI:
        第四章 引言
            第一节 研究背景及意义
            第二节 研究目的和内容
            第三节 研究方法与数据来源
        
        －－－－－－－
        """
        system_prompt_chapter = SystemMessagePromptTemplate.from_template(chapter_template)

        # 用户的询问
        user_template = "{user_input}"
        user_prompt = HumanMessagePromptTemplate.from_template(user_template)

        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_chapter, user_prompt])
        question = f'''参考以下文本回答问题：
        －－－－－－－
        文本:
        今年是{year}年,企业需要编写研究报告,根据提供的报告主题,每个章节至少有3个小节,其中包含最后两章为未来展望、结论与建议;
        大纲只细分到小节,每个小节下面不要再生成内容;
        按照顺序生成从第{chapter_begin}到第{chapter_end}章节,每个章节都要有换行符\n
        －－－－－－－
        问题:
        今年是{year}年,报告主题为中{subject}，
        已知已有{chapter_end}个章节大刚如下 其中包含最后两章为未来展望、结论与建议;
        大纲只细分到小节,每个小节下面不要再生成内容;
        按照顺序生成从第{chapter_begin}到第{chapter_end}章节,每个章节都要有换行符\n
        已知已生成了以下{have_chapter_begin}个章节大刚,目录大纲如下
        {content}
        
        请继续编写从第{chapter_begin}到第{chapter_end}章节大纲,其中包含最后两章为未来展望、结论与建议;
        大纲只细分到小节,每个小节下面不要再生成内容;
        按照顺序生成从第{chapter_begin}到第{chapter_end}章节,每个章节都要有换行符\n
        －－－－－－－
        返回固定格式样例 
        第九章 中国互联网行业结构与规模
            第一节 互联网行业分类及特点
            第二节 2019年中国互联网行业规模与结构数据
            第三节 2020年中国互联网行业发展趋势
        
        总结格式为第N章 xxxxx  \n 第N节 \n
        '''
        prompt = chat_prompt.format_prompt(user_input=question).to_messages()
        print(prompt)
        return prompt


    