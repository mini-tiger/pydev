import win32com.client



def read_word_interval(doc,start_paragraph_index, end_paragraph_index):
    content = ''
    for i in range(start_paragraph_index, end_paragraph_index):
        paragraph = doc.Paragraphs.Item(i)
    # 创建一个包含这些段落的Range
        content_range = paragraph.Range.Text.strip()

    # 获取范围内的文本并打印
        content = content  + content_range
    return content

def read_word_paragraphs(doc_path):
    # 创建 Word 应用程序对象
    word = win32com.client.Dispatch("Word.Application")

    # 打开 Word 文档
    doc = word.Documents.Open(doc_path)

    # 查找 标题1 样式位置
    heading1_paragraphs = []
    heading1_style_name = "标题 1"  # 假设 "标题 1" 是目标样式的名称
    for i in range(1, len(doc.Paragraphs) + 1):
        paragraph = doc.Paragraphs.Item(i)
        paragraph_style_name = paragraph.Style.NameLocal
        if paragraph_style_name == heading1_style_name:
            heading1_paragraphs.append(i)

    #生成各段落的范围
    context_list = []
    for i,v in enumerate(heading1_paragraphs):
        if i == len(heading1_paragraphs)-1:
            context_list.append([heading1_paragraphs[i],len(doc.Paragraphs)+1])
        else:
            context_list.append([v,heading1_paragraphs[i+1]-1])
    print(context_list)

    #打印各段落的内容
    for i in context_list:
        a=read_word_interval(doc,i[0],i[1])
        print(a)


    # 选择你想添加批注的段落，比如第2到第4段
    start_range = doc.Paragraphs.Item(context_list[0][0]).Range
    end_range = doc.Paragraphs.Item(context_list[0][1]).Range

    # 创建一个包含这些段落的Range
    comment_range = doc.Range(Start=start_range.Start, End=end_range.End)

    # 在这个Range上添加批注
    doc.Comments.Add(Range=comment_range, Text='这是一个批注')
    # 关闭 Word 文档
    doc.Close()

    # 退出 Word 应用程序
    word.Quit()

    return heading1_paragraphs


# 示例用法
doc_path = "D:\\codes\\neolink-dataset\\contract-sentinel-web\\download_files\\山西发挥算力基地优势研究报告-20240321T175447-8896.docx"  # Word 文档的路径
paragraphs_indices = read_word_paragraphs(doc_path)
for i, index in enumerate(paragraphs_indices, 1):
    print(f"Heading 1 {i}: paragraph index {index}")
