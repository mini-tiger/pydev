import langchain
from langchain.prompts.chat import MessagePromptTemplateT

from pydiff_gui.difflibparser.difflibparser import DiffCode, DifflibParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

# 设定 AI 的角色和目标
role_template_change = "你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中删减内容对服务方有什么影响，100字内"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template_change = """
"你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中删减内容对服务方有什么影响，100字内"

示例1:
  人类："服务方中断惩罚一节中，模板文本: 服务年度内第三次及后续不达标 减免用户方电力保障未达标机柜当月服务费30%或提供等额服务； 减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务； 按照该服务中断时间的3倍赔偿，赔偿执行方式为在服务期满后，免费顺延。
  修改后文本: 服务年度内第三次及后续不达标 减免用户方电力保障未达标机柜当月服务费30%或提供等额服务； 减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务； 按照该服务中断时间的3倍赔偿。"
  AI：修改后的模板合同文本对服务方的影响主要包括以下几点：
  1. 服务不达标时，服务方需要减免用户方电力保障未达标机柜当月服务费30%或提供等额服务；
  2. 服务方还需减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务；
  3. 服务方需要按照服务中断时间的3倍赔偿用户方。这些修改可能会对服务方的收入和经营造成一定影响，但同时也强调了服务方的责任。"

"""

# 设定 AI 的角色和目标
role_template_right = "你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中增加内容对服务方有什么影响，100字内"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template_right = """
"你是一名律师，根据你的专业知识，概括的分析客户方在模板合同文本中删减内容对服务方有什么影响，100字内"

示例1:
  人类："服务方中断惩罚一节中，增加文本: 服务年度内第三次及后续不达标 减免用户方电力保障未达标机柜当月服务费30%或提供等额服务； 减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务； 按照该服务中断时间的3倍赔偿，赔偿执行方式为在服务期满后，免费顺延。
  AI：增加后的模板合同文本对服务方的影响主要包括以下几点：
  1. 服务不达标时，服务方需要减免用户方电力保障未达标机柜当月服务费30%或提供等额服务；
  2. 服务方还需减免用户方带宽保障未达标带宽产品当月服务费30%或提供合同到期后顺延一个月的服务；
  3. 服务方需要按照服务中断时间的3倍赔偿用户方。这些修改可能会对服务方的收入和经营造成一定影响，但同时也强调了服务方的责任。"

"""

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

class baichuan_llm():
    def __init__(self, *args, **kwargs):
        self.prompt = None
        self.url = kwargs["url"]
        self.llm = ChatOpenAI(
            openai_api_base=self.url,  # http://120.133.83.145:8000/v1
            openai_api_key="EMPTY",
            # openai_proxy=current_app.config["OPENAI_PROXY"],
            temperature=0,
        )

    def get_resp(self, DiffCode, human_input):
        self.message_body_wrapper(DiffCode, human_input)
        return self._request_message()

    def _request_message(self):
        # 接收用户的询问，返回回答结果
        content = ""
        if self.prompt is not None:
            response = self.llm(self.prompt)
            content = response.content
            self._reset_prompt()

        return content

    def _reset_prompt(self):
        self.prompt = None

    def _valid_diffcode(self, DiffCode):
        return DiffCode in [0, 1, 2, 3]

    def message_body_wrapper(self, DiffCode, human_input):
        if self._valid_diffcode(DiffCode) == False:
            return

        system_prompt_role = MessagePromptTemplateT
        system_prompt_cot = MessagePromptTemplateT

        if DiffCode == 3:
            system_prompt_role = SystemMessagePromptTemplate.from_template(role_template_change)
            system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template_change)
        if DiffCode == 1:
            system_prompt_role = SystemMessagePromptTemplate.from_template(role_template_right)
            system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template_right)
        if DiffCode == 2:
            system_prompt_role = SystemMessagePromptTemplate.from_template(role_template_left)
            system_prompt_cot = SystemMessagePromptTemplate.from_template(cot_template_left)
        # human_input = """
        # 模板文本:	用户方合理利用服务方提供的服务，并及时提供服务实施所需必要条件，不得擅自变更使用用途，否则，对于服务不能提供、不能及时提供或网络服务不达标等不良后果，服务方不承担任何责任。
        # 修改后文本: 用户方合理利用服务方提供的服务，并及时提供服务实施所需必要条件，不得擅自变更使用用途。
        # """
        # 用户的询问
        human_template = "{human_input}"
        human_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt_role, system_prompt_cot, human_prompt])

        self.prompt = chat_prompt.format_prompt(human_input=human_input).to_messages()
