import jinja2

class PromptTpl:
    def __init__(self,**kwargs):
        self.source_term= kwargs.get("source_term", None)
        self.modify_term= kwargs.get("modify_term", None)
        self.important_terms=kwargs.get("important_terms",None)
        self.risk_warning=kwargs.get("risk_warning",None)
p=PromptTpl()
print(p.source_term)
cot_template_change = """
你是一名律师，根据你的专业知识，概括分析修改过的条款对服务方或乙方有哪些负面影响，100字内
示例1:
  原条款: {{ source_term | default('用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。',true) }}
  修改过条款 : {{ modify_term | default('未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。') }}
  AI：{{ important_terms }} 条款修改的影响:
  {{ risk_warning | default('1.有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意;2.缩小我司承接业务的模式。')}}
"""

# Example usage
source_text = ""
modify_text = "修改后的文本"
risk_warning = "风险提示"

rendered_template = jinja2.Template(cot_template_change).render(
    source_text=source_text or None,
    modify_text=modify_text or None,
    risk_warning=risk_warning or None
)

print(rendered_template)

