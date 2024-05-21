from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib import  colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
song = "simsun"
pdfmetrics.registerFont(TTFont(song, "/pdf_word_生成/font/SimSun.ttc"))

Style=getSampleStyleSheet()

bt = Style['Normal']     #字体的样式
# bt.fontName='song'    #使用的字体
bt.fontSize=14            #字号
bt.wordWrap = 'CJK'    #该属性支持自动换行，'CJK'是中文模式换行，用于英文中会截断单词造成阅读困难，可改为'Normal'
bt.firstLineIndent = 32  #该属性支持第一行开头空格
bt.leading = 20             #该属性是设置行距

ct=Style['Normal']
# ct.fontName='song'
ct.fontSize=12
ct.alignment=1            #居中

ct.textColor = colors.red

t = Paragraph('hello',bt)
pdf=SimpleDocTemplate('ppff.pdf')
pdf.multiBuild([t])

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

# .....
# ..... some exta code unimportant for this issue....
# ....

from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas
# here it is
ptr = open("demo.txt", "r")  # text file I need to convert
lineas = ptr.readlines()
ptr.close()


page_width, page_height = A4
chars_per_line = int(page_width / 6)  # 假设每个中文字符占用6个点的宽度

i = page_height - 50

i = 750
numeroLinea = 0
pdf = canvas.Canvas("/mnt/output.pdf", pagesize=letter)
while numeroLinea < len(lineas):
    if numeroLinea - len(lineas) < 60: # I'm gonna write every 60 lines because I need it like that
        i=750
        for linea in lineas[numeroLinea:numeroLinea+60]:
            pdf.setFont(song, 12)
            pdf.drawString(15, i, linea.strip())
            numeroLinea += 1
            i -= 12
        pdf.showPage()
    else:
        i = 750
        for linea in lineas[numeroLinea:]:
           pdf.setFont(song, 12)
           pdf.drawString(15, i, linea.strip())
           numeroLinea += 1
           i -= 12
        pdf.showPage()

pdf.save()