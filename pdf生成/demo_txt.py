from reportlab.lib.pagesizes import A4,inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib import  colors

# 注册中文字体
song = "simsun"
pdfmetrics.registerFont(TTFont(song, "/data/work/pydev/pdf生成/font/SimSun.ttc"))


def generate_style_pdf(content,save_pdf_path):
    doc = SimpleDocTemplate(save_pdf_path, pagesize=(A4[0], A4[1]), topMargin=1 * inch, bottomMargin=1 * inch,
                            leftMargin=0.6 * inch, rightMargin=0.6 * inch)
    Style=getSampleStyleSheet()

    bt = Style['Normal']     #字体的样式
    bt.fontName= song  #使用的字体
    bt.fontSize=12            #字号
    bt.wordWrap = 'CJK'    #该属性支持自动换行，'CJK'是中文模式换行，用于英文中会截断单词造成阅读困难，可改为'Normal'
    bt.firstLineIndent = 32  #该属性支持第一行开头空格
    bt.leading = 20             #该属性是设置行距

    ct=Style['Normal']
    # ct.fontName='song'
    ct.fontSize=12
    ct.alignment=0             #居中

    # ct.textColor = colors.red

    t = Paragraph(content,bt)
    # pdf=SimpleDocTemplate(save_pdf_path)
    # pdf.multiBuild([t])
    doc.build([t])

def generate_custom_pdf(content,save_pdf_path):
    # 计算每行的字数
    page_width, page_height = A4
    font_size = 12
    chars_per_line = int(page_width / pdfmetrics.stringWidth('中', song, font_size)) - 4   # 估算每行的字数

     #拆分文本内容为适当长度的行
    lines = [content[i:i + chars_per_line] for i in range(0, len(content), chars_per_line)]


    # print(lines)
    i = page_height - 50
    numeroLinea = 0

    # 创建 PDF 文件
    pdf = canvas.Canvas(save_pdf_path, pagesize=A4)

    for line in lines:
        # 设置中文字体
        pdf.setFont(song, font_size)

        # 绘制文本
        pdf.drawString(15, i, line)

        # 更新坐标
        i -= font_size + 2  # 加上一些间距，防止文字重叠

        # 换页处理
        if i < 0:
            pdf.showPage()
            i = page_height - 50

    pdf.save()


if __name__ == "__main__":
    # 读取文本文件
    with open("demo.txt", "r", encoding="utf-8") as file:
        content = file.read()
    generate_style_pdf(content,"/mnt/ppff.pdf")
    generate_custom_pdf(content,"/mnt/output.pdf")