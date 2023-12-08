import logging
import time
from jinja2 import Environment, FileSystemLoader
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import requests, os
from unstructured.partition.docx import partition_docx
from service.文本匹配段落 import WordDocumentParser
from service.utils import replace_str, str_valid, find_context
from exchangelib.protocol import close_connections
requests.packages.urllib3.disable_warnings()
from pytz import timezone
import sys
from word_对比转换.run_init_db import word_2_record
from pydiff_gui.difflibparser.difflibparser import DiffCode,DifflibParser
from service.确定版本 import base_valid,sjhl_valid,preset_valid,find_src_version_filename,dyx_valid,ele2lines,convert_docx_to_txt
from service.file_struct_define import dyx_unstd_reserved,undyx_unstd_reserved,dyx_unstd_unreserved,undyx_unstd_unreserved
from sqlalchemy import create_engine
from service.llm import baichuan_llm
engine = create_engine("postgresql+psycopg2://test:test123@172.22.50.25:31867/postgres")
from sqlalchemy.orm import sessionmaker

# 连接到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# 获取数据库会话
session = loadSession()

# 此句用来消除ssl证书错误，exchange使用自签证书需加上
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
# 中国时区
china_tz = timezone('Asia/Shanghai')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - Line %(lineno)d: %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger("run_mail_docx")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

base_dir = "/data/work/pydev/word_对比转换/"


class single_mail_data:
    src_txt_file = ""
    # src_doc_file = ""
    dyx = False
    reserved = False
    email_txt_file = ""
    email_doc_file = ""

    dest_unstruct_dict = {}

    dest_unstruct_elm = {}
    dest_elm = object

    # src_docparse = WordDocumentParser()
    # dest_docparse = WordDocumentParser()




class Docx_Process():
    def __init__(self, downlaod_path, convert_path, source_txt_path,baichuan_llm):
        self.download_path = downlaod_path
        self.source_txt_path = source_txt_path
        self.baichuan_llm = baichuan_llm
        self.convert_path = convert_path
        # 输入你的域账号如example\leo
        # Create a custom session with a timeout


        self.cred = Credentials(r'21VIANET\tao.jun', 'Taojun!@#')
        self.config = Configuration(server='mail.21vianet.com', credentials=self.cred, auth_type=NTLM)

        self.account = Account(
            primary_smtp_address='tao.jun@neolink.com', config=self.config, autodiscover=False, access_type=DELEGATE
        )

    def process(self):
        while 1 == 1:
            time.sleep(10)
            try:
                mail_result = self.mail_listen()
            except Exception as e:
                logger.error(f"!!!!!!1 mail_listen Fail,check Cred,account")
                continue
            logger.info(f"接收到{len(mail_result)}封邮件")
            for index, mail in enumerate(mail_result):
                email = mail["mail"]
                filenames = mail["filenames"]
                logger.info("===" * 40)
                if len(filenames) == 0:
                    logger.info(
                        f"第{index + 1} 封邮件,跳过 , 邮件内不包含附件,邮件标题:[{email.subject}],Sender:[{email.sender}] ")
                else:
                    logger.info(
                        f"第{index + 1} 封邮件,邮件内包含附件,邮件标题:[{email.subject}],Sender:[{email.sender.email_address}],文件个数:[{len(filenames)}]")

                self.single_email_process(mail)

                logger.info("===" * 40)

    def single_email_process(self, mail):
        email = mail["mail"]
        filenames = mail["filenames"]
        for index, single_mail_data in enumerate(filenames):

            logger.info("%s %s %s" % ("==" * 15, "第%s个附件开始处理" % (index + 1), "==" * 15))
            try:
                # email附件 转换 dict  elements
                self.unstruct_process(single_mail_data=single_mail_data)

                # email附件 转换 txt
                txt = self.Docx2txt(single_mail_data.email_doc_file, mail_ele=single_mail_data.dest_src_elm)
                single_mail_data.email_txt_file = txt

                # 确认版本
                record_cls, valid = self.version_valid(single_mail_data.dest_src_elm)
                if valid == False:
                    logger.error("%s %s %s" % (single_mail_data.email_doc_file, "没有匹配到模板", "==" * 15))
                    html = self.gerenate_html_fail(single_mail_data, warnings="附件文件没有匹配到模板文件,请自行审核!")
                    self.mail_send(html=html, to_recipient=[email.sender], cc_recipients=email.cc_recipients)
                else:
                    single_mail_data.dyx = record_cls.dyx
                    single_mail_data.reserved = record_cls.reserved
                    # find txt file path
                    src_txt_file_list = find_src_version_filename(source_txt_path=self.source_txt_path,
                                                                  dyx=record_cls.dyx,
                                                                  reserved=record_cls.reserved)
                    if len(src_txt_file_list) != 1:
                        logger.error(f"!!!!! src_txt_file_list: {src_txt_file_list} ,len neq 1")
                        continue
                    single_mail_data.src_txt_file = os.path.join(self.source_txt_path, src_txt_file_list[0])
                    logger.info(f"匹配到的 src_txt_file: {single_mail_data.src_txt_file} ")
                    html = self.gerenate_html_txt_diff(single_mail_data=single_mail_data)

                    self.mail_send(html=html, to_recipient=[email.sender], cc_recipients=email.cc_recipients)

            except Exception as e:
                html = self.gerenate_html_fail(single_mail_data, warnings="附件文件没有匹配到模板文件,请自行审核!")
                self.mail_send(html=html, to_recipient=[email.sender], cc_recipients=email.cc_recipients)
                logger.error("!!! Fail: %s " % (e.__str__()))

            logger.info("%s %s %s" % ("==" * 15, "第%s个附件处理结束" % (index + 1), "==" * 15))

    def version_valid(self, ele):
        file_content = ele2lines(elements=ele)
        valid = False
        record_cls = object
        if dyx_valid(file_content=file_content):
            valid = True
            if preset_valid(file_content=file_content):
                record_cls = dyx_unstd_reserved()
            else:
                record_cls = dyx_unstd_unreserved()
        # 必须满足
        if sjhl_valid(file_content) and base_valid(file_content, str="互联网信息安全责任书"):
            valid = True
            if preset_valid(file_content=file_content):
                record_cls = undyx_unstd_reserved()
            else:
                record_cls = undyx_unstd_unreserved()

        return record_cls, valid

    def unstruct_process(self, single_mail_data):
        # elements = partition_docx(filename=single_mail_data.src_doc_file)
        elements1 = partition_docx(filename=single_mail_data.email_doc_file)
        single_mail_data.dest_src_elm = elements1
        for i in elements1:
            single_mail_data.dest_unstruct_dict[replace_str(i.text)] = {"id": i.id, "parent_id": i.metadata.parent_id,
                                                                        "page_number": i.metadata.page_number}
            single_mail_data.dest_unstruct_elm[i.id] = i.text

    def Docx2txt(self, file_path, mail_ele):
        file_name = os.path.basename(file_path)  # Gets the file name with extension
        file_name_list = os.path.splitext(file_name)  # Gets the file extension
        file_ext = file_name_list[1]
        file_name_real = file_name_list[0]
        out_file = os.path.join(self.convert_path, file_name_real + ".txt")
        # with open(out_file, 'w', encoding='utf-8') as outfile:
        #     doc = docx2txt.process(file_path)
        #     outfile.write(doc)

        with open(out_file, "w") as f:
            for i in mail_ele:
                f.write(i.text)
                f.write("\n")
        return out_file

    def mail_send(self, html, to_recipient=[], cc_recipients=[]):
        # Create a message object
        m = Message(account=self.account, subject='HTML Email Test', body='This is the body of the email in plain text')

        # Attach the HTML content to the email
        m.body = HTMLBody(html)
        # m.is_html = True  # Specify that the body content is HTML

        # Set the recipient's email address
        m.to_recipients = to_recipient
        m.cc_recipients = cc_recipients
        # Send the email
        m.send_and_save()

    def mail_listen(self):
        # 收取未读邮件
        unread_emails = self.account.inbox.filter(is_read=False)
        accepted_extensions = ['doc', 'docx']

        mail_result = []
        for email in unread_emails:
            # 获取邮件标题和正文内容
            # 获取发件人和发件时间

            filenames = []
            # 检查邮件是否含有附件
            if not email.attachments:
                pass
                # return mail_result
            else:
                for attachment in email.attachments:
                    # 下载邮件附件
                    filename, file_extension = attachment.name.rsplit('.', 1)
                    file_extension = file_extension.lower()
                    single_data = single_mail_data()
                    # 如果扩展名在接受的列表中，下载附件
                    if file_extension in accepted_extensions:
                        filename = os.path.join(self.download_path, attachment.name)
                        single_data.email_doc_file = filename
                        filenames.append(single_data)
                        with open(filename, 'wb') as f:
                            f.write(attachment.content)
            # xxx 标记邮件为已读
            email.is_read = True
            email.save()
            mail_result.append({"mail": email, "filenames": filenames})
        close_connections()
        return mail_result

    def gerenate_html_fail(self, single_mail_data, **kwargs):
        txt_file_email = single_mail_data.email_txt_file

        # Load the Jinja2 template
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')

        # Render the template with the dynamic content
        html_output = template.render(lines=[], src_docx_file="",
                                      email_file=os.path.basename(single_mail_data.email_doc_file), **kwargs)
        #
        # with open('diff_output_custom_parser.html', 'w', encoding='utf-8') as file:
        #     file.write(html_output)
        return html_output

    def gerenate_html_txt_diff(self, single_mail_data):

        txt_file_std = single_mail_data.src_txt_file
        txt_file_email = single_mail_data.email_txt_file

        with open(txt_file_std, 'r') as file1, open(txt_file_email, 'r') as file2:
            src_content = file1.readlines()
            mail_content = file2.readlines()

        differ = DifflibParser(src_content, mail_content)
        line_number = 0
        lines = []

        for line in differ:
            if line['code'] > 0:
                part = ""
                page = ""

                effect = ""
                risk= ""
                row = line["line"]
                if str_valid(row):
                    continue
                line_number += 1

                if line['code'] == DiffCode.LEFTONLY:

                    type = "附件比模板减少的内容"

                    lca = session.query(word_2_record).filter(word_2_record.dyx == single_mail_data.dyx,
                                                              word_2_record.reserved == single_mail_data.reserved,
                                                              word_2_record.content.like(f'%{replace_str(row)}%')).all()
                    if len(lca) > 0:
                        page = "\nor\n".join([i.page_number for i in lca])
                        part = "\nor\n".join([i.part for i in lca])
                        risks_list = lca[0].risk_impact
                        risk="\n".join([v.risk_warning for v in risks_list if v.focus.find("left") != -1])
                        # context = lca[0].content
                    # result = single_mail_data.src_docparse.find_paragraph_by_text(target_text=replace_str(line["line"]))
                    # context=result['section_info']

                    if part != "":
                        human_input = f"""
                        减少内容文本:	{replace_str(row)} 
                        """
                        logger.info("大模型QA: %s"%replace_str(human_input))
                        effect=self.baichuan_llm.get_resp(DiffCode.LEFTONLY,human_input)
                    line_info = {
                        'number': line_number,
                        'type': type,
                        'page': page,
                        'part': part,
                        'result': f'<span style="background-color: #ff9999;">{row}</span>',
                        'effect':effect,
                        'risk':risk
                    }

                elif line['code'] == DiffCode.RIGHTONLY:
                    type = "模板中不存在的内容"
                    Sentence = ""

                    # xxx 找到目标行的 parentid
                    if single_mail_data.dest_unstruct_dict.get(replace_str(row)):
                        rc = single_mail_data.dest_unstruct_dict[replace_str(row)]

                        if single_mail_data.dest_unstruct_elm.get(rc["parent_id"]):
                            # print("dest doc", dest_unstruct_elm[rc["parent_id"]])
                            Sentence = single_mail_data.dest_unstruct_elm[rc["parent_id"]]
                            # if len(Sentence) > 2:

                        # xxx  没有parentid
                        else:
                            Sentence = find_context(elem=single_mail_data.dest_src_elm, target_str=replace_str(row),
                                                    up=1)

                    lca = session.query(word_2_record).filter(word_2_record.dyx == single_mail_data.dyx,
                                                              word_2_record.reserved == single_mail_data.reserved,
                                                              word_2_record.content.like(
                                                                  f'%{replace_str(Sentence)}%')).all()
                    if len(lca) > 0:
                        page = lca[0].page_number
                        part = lca[0].part
                    # result = single_mail_data.dest_docparse.find_paragraph_by_text(target_text=replace_str(row))
                    # context = result['section_info']
                    if part != "":
                        human_input = f"""
                        增加内容文本:	{replace_str(line["line"])} 
                        """
                        logger.info("大模型QA: %s"%replace_str(human_input))
                        effect=self.baichuan_llm.get_resp(DiffCode.RIGHTONLY,human_input)
                    line_info = {
                        'number': line_number,
                        'type': type,
                        'page': page,
                        'part': part,
                        'result': f'<span style="background-color: #99ff99;">{replace_str(row)}</span>',
                        'effect': effect
                    }

                elif line['code'] == DiffCode.CHANGED:
                    type = "模板与附件内容不同"
                    leftchanges = line.get('leftchanges', [])
                    rightchanges = line.get('rightchanges', [])
                    new_line = list(line['newline'])

                    # Highlight individual different characters in red and green
                    for i in range(len(new_line)):
                        if i in leftchanges:
                            new_line[i] = f'<span style="background-color: #ff9999;">{new_line[i]}</span>'
                        if i in rightchanges:
                            new_line[i] = f'<span style="background-color: #99ff99;">{new_line[i]}</span>'

                    lca = session.query(word_2_record).filter(word_2_record.dyx == single_mail_data.dyx,
                                                              word_2_record.reserved == single_mail_data.reserved,
                                                              word_2_record.content.like(f'%{replace_str(row)}%')).all()
                    if len(lca) > 0:
                        page = "\nor\n".join([i.page_number for i in lca])
                        part = "\nor\n".join([i.part for i in lca])
                        risks_list = lca[0].risk_impact
                        risk="\n".join([v.risk_warning for v in risks_list if v.focus.find("left") != -1])
                        # context = lca[0].content
                    # result = single_mail_data.dest_docparse.find_paragraph_by_text(target_text=replace_str(line["newline"]))
                    # context=result['section_info']
                    if part != "":
                        human_input = f"""
                        模板文本:	{replace_str(line["line"])} \n
                        修改后文本: {replace_str(line["newline"])}
                        """
                        logger.info("大模型QA: %s"%replace_str(human_input))
                        effect=self.baichuan_llm.get_resp(DiffCode.CHANGED,human_input)
                    line_info = {
                        'number': line_number,
                        'type': type,
                        'page': page,
                        'part': part,
                        'result': f'<span style="background-color: #99ff99;">{"".join(new_line)}</span>',
                        'effect': effect,
                        'risk':risk
                    }


                else:
                    # html_output += f'<td>{line["line"]}</td></tr>'
                    continue

                lines.append(line_info)
        src_docx_file = (os.path.basename(txt_file_std).split("_", 3))[3].replace(".txt", ".docx")
        # Load the Jinja2 template
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')

        # Render the template with the dynamic content
        html_output = template.render(lines=lines, src_docx_file=src_docx_file,
                                      email_file=os.path.basename(single_mail_data.email_doc_file))
        logger.info(f"total risk line info:{len(lines)}")
        #
        # with open('diff_output_custom_parser.html', 'w', encoding='utf-8') as file:
        #     file.write(html_output)
        return html_output


# 1. 加上抄送人
# 2. 匹配 不到的模板 要提示
# 3。 显示模板文件名称
if __name__ == "__main__":
    os.environ.get()
    source_docs_path = "/data/work/pydev/word_对比转换/source_docx"
    source_txt_path = "/data/work/pydev/word_对比转换/source_txt"
    # 所有 docx 转换txt
    txt_dict, txt_list = convert_docx_to_txt(src_doc_dir=source_docs_path, txt_dir=source_txt_path)
    baichuan_url="http://120.133.83.145:8000/v1"
    Docx_Process(downlaod_path=os.path.join(base_dir, "download_test"),
                 convert_path="/data/work/pydev/word_对比转换/convert_test",
                 source_txt_path=source_txt_path,baichuan_llm=baichuan_llm(url=baichuan_url)).process()
