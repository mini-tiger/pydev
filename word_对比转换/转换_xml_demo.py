import zipfile
import xml.etree.ElementTree as ET

def read_word_document(docx_path):
    # Open the Word document using zipfile
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        # Extract the content of the document.xml file
        xml_content = zip_ref.read('word/document.xml')

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Extract and print some information from the document
    for paragraph in root.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
        text = ''
        for run in paragraph.findall('.//w:r', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            for t in run.findall('.//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                text += t.text if t.text else ''
        print(text)

# Example usage
docx_path = '/data/work/pydev/word_对比转换/unlock_unstatic.docx'
read_word_document(docx_path)
