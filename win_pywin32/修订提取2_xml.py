from docx import Document
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

word_body = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
text_tag  = word_body + "t"
del_tag   = word_body + "delText"
ins_tag   = word_body + "ins"

def accept_all(p):
    """Return text of a paragraph after accepting all changes"""
    xml = p._p.xml
    tree = XML(xml)
    runs = (node.text for node in tree.iter(text_tag) if node.text)
    if "w:del" in xml :
        return f'adel:{"".join(runs)}'
    if "w:ins" in xml:
        return f'ains:{"".join(runs)}'
    # else:
    #     return p.text

def reject_all(p):
    """Return text of a paragraph after rejecting all changes"""
    xml = p._p.xml
    if "w:del" in xml or "w:ins" in xml:
        tree = XML(xml)
        # find and remove all insert tags
        for insert in tree.findall(ins_tag):
            tree.remove(insert)
        # find all deletion tags and change to text tags
        for deletion in tree.iter(del_tag):
            deletion.tag = text_tag
        runs = (node.text for node in tree.iter(text_tag) if node.text)
        return f'reject:{"".join(runs)}'
    # else:
    #     return p.text

doc = Document(r"G:\codes\python\pydev\win_pywin32\output_document.docx")

for index,p in enumerate(doc.paragraphs):
    print(f"line:{index}")

    print("---")
    print(p.text)
    print("---")
    print(accept_all(p))
    print("=========")
    print(reject_all(p))
    print("=========")