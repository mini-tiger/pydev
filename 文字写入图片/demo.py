from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(input_image_path, output_image_path, text, position=(10, 10), text_color=(255, 255, 255), font_size=20):
    # 打开图片
    image = Image.open(input_image_path)

    # 创建Draw对象
    draw = ImageDraw.Draw(image)

    # 选择字体和大小
    font = ImageFont.truetype("/data/work/pydev/pdf生成/font/SimSun.ttc", font_size)

    # 在指定位置写入文字
    draw.text(position, text, font=font, fill=text_color)

    # 保存修改后的图片
    image.save(output_image_path)

# 指定输入图片和输出图片的路径
input_image_path = 'demo.jpg'
output_image_path = 'output.jpg'

# 要添加的文字和其他参数
text_to_add = '我是测试 Hello, World!'
text_position = (50, 50)
text_color = (255, 0, 0)  # RGB颜色
font_size = 30

# 调用添加文字的函数
add_text_to_image(input_image_path, output_image_path, text_to_add, text_position, text_color, font_size)
