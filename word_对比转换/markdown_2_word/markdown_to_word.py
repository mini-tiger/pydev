from word_对比转换.markdown_2_word.utils.Markdown2docx import Markdown2docx

project = Markdown2docx('test')

project.style_table="Table Grid"
project.eat_soup()
from docx.shared import RGBColor
project.write_html()  # optional
print(type(project.styles()))
for k, v in project.styles().items():
    print(f'stylename: {k} = {v}')


# 设置所有字体的颜色
def set_font_color(doc, color):
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = color


# 定义颜色（例如红色）
color = RGBColor(0, 0, 0)

# 应用颜色设置
set_font_color(project.doc, color)

project.outfile= "/mnt/191/test.docx"
project.save()