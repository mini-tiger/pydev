from docx2python import docx2python

# extract docx content
with docx2python('/data/work/pydev/word_对比转换/unlock_unstatic.docx') as docx_content:
    print(docx_content.text)

docx_content = docx2python('/data/work/pydev/word_对比转换/unlock_unstatic.docx')
print(docx_content.text)
docx_content.close()

# extract docx content, write images to image_directory
with docx2python('/data/work/pydev/word_对比转换/unlock_unstatic.docx', 'path/to/image_directory') as docx_content:
    print(docx_content.text)

# extract docx content with basic font styles converted to html
with docx2python('/data/work/pydev/word_对比转换/unlock_unstatic.docx', html=True) as docx_content:
    print(docx_content.text)