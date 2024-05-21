from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import utils

# 创建 PDF 文档
pdf_path = "/mnt/pdf/output.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)

# 图片路径
image_path = "bar.png"  # 替换为你的图片路径

# 获取图片信息
img = utils.ImageReader(image_path)
img_width, img_height = img.getSize()

# 设置 A4 页面的宽度
a4_width = A4[0]

# 计算缩放比例
scale_factor = a4_width / img_width

# 计算缩放后的图片高度
scaled_height = img_height * scale_factor

# 插入图片并设置大小
c.drawInlineImage(image_path, 0, 0, width=a4_width, height=scaled_height)

# 添加文本
c.drawString(100, 500, "Hello, ReportLab!")

# 保存并关闭 PDF 文档
c.save()

print(f"PDF created at: {pdf_path}")
