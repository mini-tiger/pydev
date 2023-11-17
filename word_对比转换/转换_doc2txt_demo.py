import docx2txt

# extract text
# text = docx2txt.process("file.docx")

# extract text and write images in /tmp/img_dir
with open("/data/work/pydev/word_对比转换/unlock_unstatic.docx" + '.txt', 'w', encoding='utf-8') as outfile:
    doc = docx2txt.process("/data/work/pydev/word_对比转换/unlock_unstatic.docx")
    outfile.write(doc)

with open("/data/work/pydev/word_对比转换/unlock_unstatic_modify.docx" + '.txt', 'w', encoding='utf-8') as outfile:
    doc = docx2txt.process("/data/work/pydev/word_对比转换/unlock_unstatic_modify.docx")
    outfile.write(doc)