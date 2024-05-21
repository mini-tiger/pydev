import pdfkit

def html_to_pdf(html_content, output_path):
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        "enable-local-file-access": None
    }

    pdfkit.from_string(html_content, output_path, options=options)

# 示例 HTML 内容
html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>HTML to PDF Example中文</title>

</head>
<body>
    <h1>Hello, PDFKit!</h1>
    <p>This is a simple example of converting HTML to PDF using pdfkit.中文</p>
    <img src="./bar.png" alt="Big Boat">
</body>
</html>
"""

# 输出 PDF 文件路径
output_pdf_path = "output.pdf"

# 进行 HTML 到 PDF 的转换
html_to_pdf(html_content, output_pdf_path)

print(f"PDF created at: {output_pdf_path}")


import pdfkit

wkhtmltopdf_options = {
    'page-size': 'A4',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'enable-local-file-access': None
}

pdfkit.from_file("./1.html", 'out1.pdf', options=wkhtmltopdf_options)