from docx import Document

def get_chapter_numbers(doc):
    chapter_numbers = []
    sections = doc.sections
    for section in sections:
        print(section.start_type)
    for paragraph in doc.paragraphs:

        style = paragraph.style.name.lower()
        print(paragraph.text)
        print(style)
        if 'heading' in style and 'chapter' in style:
            # 获取章节编号
            chapter_number = paragraph.text.strip().split()[1]
            chapter_numbers.append(chapter_number)

    return chapter_numbers

def main():
    # 替换为你的Word文档路径
    doc_path = r"G:\codes\python\pydev\win_pywin32\output_document.docx"

    # 打开文档
    doc = Document(doc_path)

    # 获取章节序号
    chapter_numbers = get_chapter_numbers(doc)

    # 打印章节序号
    for i, number in enumerate(chapter_numbers, start=1):
        print(f"Chapter {i}: {number}")

if __name__ == "__main__":
    main()
