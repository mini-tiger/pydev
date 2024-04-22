import langchain
from langchain.prompts.chat import MessagePromptTemplateT
from jinja2 import Template
from service.utils import replace_str
from service.g import logger
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

# left change
# 使用pywin32 source_page_dict[replace_str"文本"]=page,part等
# right
# 使用pywin32 mail_page_dict["文本"]=page,part

# 提取 修订项 ，
# 1.先判断是否跳过（关键字）
# 2.line 与找16个对象 每个 匹配,json规则 不用存DB，用ID区分建立 不同的类实例，匹配不到用 通用的实例



# 设定 AI 的角色和目标
role_template_change = "你是一名律师，根据你的专业知识，概括分析修改过的条款对服务方或乙方有哪些负面影响，100字内"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template_change = """
{{ hint | default('%s') }}
示例1:
  原条款: {{ source_text| default('用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。') }}
  修改过条款 : {{ modify_text | default('未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。') }}
  AI：影响：
  {{ risk_warning | default('1.有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意;2.缩小我司承接业务的模式。')}}
""" %(role_template_change)

cot_template_rule_change = """
{{ hint | default('%s') }}
示例1:
  条款: {{ examples_terms }}
  AI：影响：
  {{ risk_warning }}
""" %(role_template_change)


# 设定 AI 的角色和目标
role_template_right = "你是一名律师，根据你的专业知识，概括分析增加的条款对服务方或乙方有哪些负面影响，100字内"

cot_template_right = """
{{ hint | default('%s') }}
示例1:
  增加的条款 : {{ add_text | default('合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。') }}
  AI：影响：
  {{ risk_warning | default('1.不可能因为一个公司放弃一个行业，导致我司业务发展受限。;2.缩小我司承接业务的模式。')}}
""" %(role_template_right)

# 设定 AI 的角色和目标
role_template_left = "你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中删减内容对服务方有什么影响，100字内"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template_left = """
你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中删减内容对服务方有什么影响，100字内

示例1:
  人类：在合同 服务标准 一节中 减少内容文本:服务年度内第三次及后续不达标 减免用户方电力保障未达标机柜当月服务费30%或提供等额服务； 减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务； 按照该服务中断时间的3倍赔偿，赔偿执行方式为在服务期满后，免费顺延
  AI：服务方可能面临以下风险：
    1. 减少了对不达标服务的处罚措施，可能导致服务方对用户方的服务质量降低；
    2. 减少了对带宽保障不达标的处罚措施，可能影响服务方的带宽服务质量；
    3. 减少了赔偿方式，可能导致服务方在服务中断时的赔偿不足，影响用户方的利益。

"""
import os
class baichuan_llm():
    def __init__(self, *args, **kwargs):
        self.prompt = None
        self.url = kwargs["url"]

        self.llm = ChatOpenAI(
            openai_api_base=self.url,  # http://120.133.83.145:8000/v1
            openai_api_key="EMPTY",
            model_name="Baichuan2-13B-Chat",
            # openai_proxy=kwargs["proxy"],
            temperature=0,
            request_timeout=120
        )


    def get_resp(self, DiffCode, line,system_prompt_cot_custom=None):
        self.message_body_wrapper(DiffCode, line, system_prompt_cot_custom)
        return self._request_message()

    def get_resp_custom_tpl(self,DiffCode,cot_template,human_input):
        # 用户的询问
        human_template = "{human_input}"
        human_prompt = HumanMessagePromptTemplate.from_template(human_template)

        system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template)
        # print(human_prompt)
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_cot, human_prompt])
        # print(chat_prompt.messages)
        # print(human_input)

        self.prompt = chat_prompt.format_prompt(human_input=human_input).to_messages()
        return self._request_message()

    def _request_message(self):
        # 接收用户的询问，返回回答结果
        content = ""
        if self.prompt is not None:
            try:
                response = self.llm(self.prompt)
                content = response.content
            except Exception as e:
                logger.error(str(e))
                return ''

        self._reset_prompt()
        return content

    def _reset_prompt(self):
        self.prompt = None

    def _valid_diffcode(self, DiffCode):
        return DiffCode in [0, 1, 2, 3]

    def message_body_wrapper(self, DiffCode, line,system_prompt_cot_custom=None,**kwargs):
        if self._valid_diffcode(DiffCode) == False:
            return

        # system_prompt_role = MessagePromptTemplateT
        system_prompt_cot = MessagePromptTemplateT
        human_input=""
        if DiffCode == 3:
            # 创建 Jinja2 模板对象
            template = Template(cot_template_change)
            # 渲染模板，传递变量
            rendered_output = template.render(kwargs)
            # system_prompt_role = SystemMessagePromptTemplate.from_template(role_template_change)
            system_prompt_cot = SystemMessagePromptTemplate.from_template(rendered_output)
            human_input = f"""{role_template_change}\n
            原条款:{replace_str(line["line"])}
            修改过条款:{replace_str(line["newline"])}"""

        if DiffCode == 1:
            human_input = f"""{role_template_right}\n
            减少内容文本:	{replace_str(line['line'])} 
            """
            # system_prompt_role = SystemMessagePromptTemplate.from_template(role_template_right)
            system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template_right)
        if DiffCode == 2:
            human_input = f"""{role_template_left} \n
            增加的条款:	{replace_str(line['line'])}
            """
            # system_prompt_role = SystemMessagePromptTemplate.from_template(role_template_left)
            system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template_left)

        if system_prompt_cot_custom is not None:
            system_prompt_cot=system_prompt_cot_custom
            # print(system_prompt_cot_custom)
        else:
            pass
            # print(system_prompt_cot)
        # 用户的询问
        human_template = "{human_input}"
        human_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # print(human_prompt)
        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_cot, human_prompt])
        # print(chat_prompt.messages)
        # print(human_input)
        self.prompt = chat_prompt.format_prompt(human_input=human_input).to_messages()

# if __name__ == "__main__":
#     llm=baichuan_llm(url="http://120.133.83.145:8000/v1")
#     from run_init_db import change_cot_default,match_data_list
#     user_tpl=match_data_list[11]["change_tpl_cot"]
#
#
#     effect = llm.get_resp_custom_tpl(DiffCode=3, cot_template=change_cot_default, human_input=user_tpl)
#     print(effect)