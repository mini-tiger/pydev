import logging
import sys
# 设定 AI 的角色和目标
role_template_change = "你是一名律师，根据你的专业知识，概括的分析条款对服务方或乙方有哪些影响，100字内"

# CoT 的关键部分，AI 解释推理过程，并加入一些先前的对话示例（Few-Shot Learning）
cot_template_change = """
{{ hint | default('你%s') }}
示例1:
  条款: {{ example_terms | default('未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。') }}
  AI：对服务方的影响主要包括：
  {{ risk_warning | default('有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意;缩小我司承接业务的模式。')}}
""" %(role_template_change)

from jinja2 import Template


# 创建 Jinja2 模板对象
template = Template(cot_template_change)

# 渲染模板，传递变量
rendered_output = template.render()

# 打印渲染后的结果
print(rendered_output)