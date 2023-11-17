import zipfile
import xml.etree.ElementTree as ET


class WordDocumentParser:
    def __init__(self, docx_path):
        self.docx_path = docx_path
        self.root = self.__get_root()

    def __get_root(self):
        with zipfile.ZipFile(self.docx_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
        return ET.fromstring(xml_content)

    def read_document(self):
        text_content = []
        for paragraph in self.root.findall('.//w:p', namespaces={
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            text = ''
            for run in paragraph.findall('.//w:r', namespaces={
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                for t in run.findall('.//w:t',
                                     namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                    text += t.text if t.text else ''
            text_content.append(text)

        return text_content

    def find_paragraph_by_text(self, target_text):
        for i, paragraph in enumerate(self.root.findall('.//w:p', namespaces={
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}), 1):
            text = ''
            for run in paragraph.findall('.//w:r', namespaces={
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                for t in run.findall('.//w:t',
                                     namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                    text += t.text if t.text else ''
            if target_text in text:
                section_info = self.__get_section_info(paragraph)
                context_before, context_after = self.get_context(i, target_text)
                return {'paragraph_number': i, 'section_info': section_info, 'context_before': context_before,
                        'context_after': context_after}
        return {'paragraph_number': "", 'section_info': "", 'context_before': "",
                        'context_after': ""}

    def __get_section_info(self, paragraph):
        heading_level = None
        heading_text = ''
        for run in paragraph.findall('.//w:r',
                                     namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            for style in run.findall('.//w:pStyle',
                                     namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                heading_level = int(
                    style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val').replace('Heading',
                                                                                                           ''))
                break
            for t in run.findall('.//w:t',
                                 namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                heading_text += t.text if t.text else ''

        higher_level_section_number = self.__get_higher_level_section_number(paragraph)

        return {'heading_level': heading_level, 'heading_text': heading_text,
                'higher_level_section_number': higher_level_section_number}

    def __get_higher_level_section_number(self, paragraph):
        # Extract the higher-level section number (assuming format like '1.1', '1.2', etc.)
        higher_level_section_number = ''
        for run in paragraph.findall('.//w:r',
                                     namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            for t in run.findall('.//w:t',
                                 namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
                higher_level_section_number += t.text if t.text else ''

        return higher_level_section_number

    def get_context(self, paragraph_number, target_text):
        context_before = ''
        context_after = ''

        # Get text before the target text
        for i in range(max(1, paragraph_number - 2), paragraph_number):
            context_before += ' '.join(self.read_document()[i - 1].split()[-10:]) + ' '

        # Get text after the target text
        for i in range(paragraph_number, min(paragraph_number + 2, len(self.read_document())) + 1):
            context_after += ' '.join(self.read_document()[i - 1].split()[:10]) + ' '

        return context_before.strip(), context_after.strip()



if __name__ == "__main__":
    # Example usage
    doc_path = '/data/work/pydev/word_对比转换/download_test/带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）_modify.docx'
    word_parser = WordDocumentParser(doc_path)

    # Find the paragraph containing a specific text and get the context
    target_text = "带宽/DCSS/MPLS VPN/SD-WAN中断时间：由服务方造成的用户方设备不连通的时间（分钟数），但不包括带宽/DCSS/MPLS VPN/SD-WAN中断的24小时之内用户方未向服务方报告的情况，以及由以下原因所导致的用户方带宽/DCSS/MPLS VPN/SD-WAN："
    result = word_parser.find_paragraph_by_text(target_text)

    if result:
        print(f"Paragraph {result['paragraph_number']} contains '{target_text}'.")
        print(f"Section Info: {result['section_info']}")
        print(f"Context Before: {result['context_before']}")

