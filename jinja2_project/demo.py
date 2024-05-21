

from jinja2 import Template

# 读取模板文件内容
with open('tpl.jinja2', 'r') as file:
    template_content = file.read()

# 创建 Jinja2 模板对象
template = Template(template_content)

# 定义模板中的变量
context = {"messages":[{"role":"system","content":"abc"},{"role":"user","content":"bcd"}]}

# 渲染模板并输出结果
rendered_content = template.render(context)

print(rendered_content)