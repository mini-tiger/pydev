from docx import Document

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML


WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TEXT = WORD_NAMESPACE + "t"


def get_accepted_text(p):
    """Return text of a paragraph after accepting all changes"""
    xml = p._p.xml
    if "w:del" in xml or "w:ins" in xml:
        tree = XML(xml)
        runs = (node.text for node in tree.iter(TEXT) if node.text)
        # Note: on older versions it is `tree.getiterator` instead of `tree.iter`
        return "11111".join(runs)
    else:
        # return p.text
        pass


doc = Document(r"G:\codes\python\pydev\win_pywin32\a.docx")

for p in doc.paragraphs:
    # print(p.text)
    print("---")
    print(get_accepted_text(p))
    print("=========")