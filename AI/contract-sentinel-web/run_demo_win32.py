
import copy
import traceback
import time,ast
from jinja2 import Environment, FileSystemLoader
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody,FileAttachment
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

# from unstructured.partition.docx import partition_docx
from jinja2 import Template

from service.utils import replace_str, str_valid, create_directory_if_not_exists, find_closest_value, any_match, \
    all_match
from exchangelib.protocol import close_connections
import urllib3

from tools.utils import format_sse_json

urllib3.disable_warnings()

from pydiff_gui.difflibparser.difflibparser import DiffCode, DifflibParser
import sys
# from run_init_db import word_2_record, risk_impact
from service_win32.utils import docfilename_to_txtfilename,word2txt,create_directory_if_not_exists,create_revisions_docx,deny_word_revision,\
    word_deny_filename_build,rebuild_page_word_comments_write_with_dict,word_table_output
from service_win32.确定版本 import base_valid, sjhl_valid, preset_valid, find_src_version_filename, dyx_valid, \
    ele2lines, convert_docx_to_txt, ele2txt, version_valid_search, zhongzi_valid_search


from service.llm import *

from service.g import logger, ContractException, risk_keywords_dict, risk_json_record

from run_init_db import *
# 此句用来消除ssl证书错误，exchange使用自签证书需加上
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
os.environ.pop("PROCESSOR_ARCHITEW6432",None)

from dataclasses import dataclass,field
import os
import shutil
import tempfile

# 获取临时目录的路径
temp_directory = tempfile.gettempdir()

# 构造 gen_py 目录的完整路径
gen_py_path = os.path.join(temp_directory, "gen_py")

# 检查该目录是否存在
if os.path.exists(gen_py_path):
    # 递归删除 gen_py 目录
    shutil.rmtree(gen_py_path)
    print(f"Deleted '{gen_py_path}'")
else:
    print(f"The directory '{gen_py_path}' does not exist.")



@dataclass
class SingleMailData:
    src_txt_file : str=""
    src_doc_file : str= ""
    src_text_dict:dict =field(default_factory=dict)
    src_text_mapping: dict =field(default_factory=dict)
    dyx : bool = field(default=False)
    reserved : bool=field(default=False)
    email_txt_file : str= ""
    email_doc_file : str= ""
    email_text_dict: dict =field(default_factory=dict)
    email_text_mapping: dict =field(default_factory=dict)
    standpoint: str= "1"
    zhongzi: bool = field(default=False)
    zhongzi_soft: bool =field(default=False)
    zhongzi_hard: bool =field(default=False)
    word_table_output: dict = field(default_factory=dict)
    result_risk : dict =field(default_factory=dict)#  原始文本 {收缩文本:{risk:"",model_result:"",part:"",diff_type:""}}

class EmailProcess():
    def __init__(self, download_path, convert_path, template_path, source_txt_path, baichuan_llm, *args, **kwargs):
        self.download_path = download_path
        self.source_txt_path = source_txt_path
        self.baichuan_llm = baichuan_llm
        self.convert_path = convert_path
        self.template_path = template_path
        create_directory_if_not_exists(download_path)
        create_directory_if_not_exists(convert_path)
        create_directory_if_not_exists(source_txt_path)

        # 输入你的域账号如example\leo
        # Create a custom session with a timeout
        # self.cred = Credentials(r'21VIANET\liu.hao8', r'Asdfg$12345')

        # self.account = Account(
        #     primary_smtp_address='liu.hao8@neolink.com', config=self.config, autodiscover=False, access_type=DELEGATE
        # )
        # self.cred = Credentials(r'21VIANET\tao.jun', r'Taojun!@#')
        # self.config = Configuration(server='mail.21vianet.com', credentials=self.cred, auth_type=NTLM)
        # self.account = Account(
        #     primary_smtp_address='tao.jun@neolink.com', config=self.config, autodiscover=False, access_type=DELEGATE
        # )
        self.cred= Credentials(config.MAIL_CRED_USER,config.MAIL_CRED_PWD)
        self.config = Configuration(server='mail.21vianet.com', credentials=self.cred, auth_type=NTLM)
        self.account = Account(
            primary_smtp_address=config.MAIL_ACCOUNT, config=self.config, autodiscover=False, access_type=DELEGATE
        )
    def handle_process(self):
        logger.info(f"当前邮件账户为: {config.MAIL_ACCOUNT}, 邮箱用户名: {config.MAIL_CRED_USER}")
        while 1 == 1:
            try:
                mail_result = self.mail_listen()
            except Exception as e:
                logger.error(f"!!!!!! mail_listen Fail,check Cred,account,error:{e.__str__()}")
                continue
            logger.info(f"接收到{len(mail_result)}封邮件")
            for index, mail in enumerate(mail_result):
                email = mail["mail"]
                filenames = mail["filenames"]
                logger.info("===" * 40)
                if len(filenames) == 0:
                    logger.info(
                        f"第{index + 1} 封邮件,跳过,邮件内不包含附件,邮件标题:[{email.subject}],Sender:[{email.sender}] ")
                else:
                    logger.info(
                        f"第{index + 1} 封邮件,邮件内包含附件,邮件标题:[{email.subject}],Sender:[{email.sender.email_address}],文件个数:[{len(filenames)}]")

                self.attachments_handle_process(mail)

                logger.info("===" * 40)
            time.sleep(60)

    def clean(self,single_mail_data):
        # 获取实例的属性字典的副本
        attributes_copy = vars(single_mail_data).copy()
        # 遍历并删除实例中的所有属性
        for attribute_name in attributes_copy:
            delattr(single_mail_data, attribute_name)
    def attachments_handle_process(self, mail: dict):
        email = mail["mail"]
        filenames = mail["filenames"]
        print(filenames)

        for index, single_mail_data in enumerate(filenames):
            logger.info("%s %s %s" % ("==" * 15, "第%s个附件 %s 开始处理" % (index + 1,single_mail_data.email_doc_file), "==" * 15))

            html, attachments,error,error_str = DocxProcess(convert_path=config.CONVERT_PATH,
                                           template_path=config.TEMPLATE_DIR,
                                           source_txt_path=config.SOURCE_TXT_PATH,
                                           source_docs_path=config.SOURCE_DOCS_PATH,
                                           diff_docs_path=config.DIFF_DOCS_PATH,
                                           single_mail_data=single_mail_data,
                                           match_data_list=match_data_list,
                                           baichuan_llm=baichuan_llm(url=config.OPENAI_API_BASE,
                                                                     proxy=config.PROXY)).single_attachment_handle_process()

            if email.cc_recipients is None:
                email.cc_recipients = []

            # recipient_mailbox = Mailbox(email_address='tao.jun@neolink.com', name='tao.jun')
            # email.cc_recipients.append(recipient_mailbox)

            if error == False:
                self.mail_send(html=html,attachments=attachments, to_recipient=email.to_recipients, cc_recipients=email.cc_recipients)
                # xxx 日志mail
                # send mail to tao, write log.txt
                self.mail_send_log(email=email,
                                   html=html,
                                   attachments=[attachments,single_mail_data.email_doc_file],
                                   to_recipient=[Mailbox(email_address='tao.jun@neolink.com', name='tao.jun'),Mailbox(email_address='sun.mingrui@neolink.com', name='sun.mingrui')],
                                   cc_recipients=[])
            else:
                logger.info(f"!!!! Error is not None ,skip send mail {error} ")


            logger.info("%s %s %s" % ("==" * 15, "第%s个附件处理结束" % (index + 1), "==" * 15))
            # xxx write log.txt
            self.record_log(error,error_str,email,single_mail_data.email_doc_file)
            # 清理
            self.clean(single_mail_data)

    def record_log(self,error,error_str,email,email_doc_file):

        data=f"datetime_created:[{email.datetime_created.now()}],error:[{error}],error_str:[{error_str}] , attachments:[{email_doc_file}]"
        # 打开文件，如果文件不存在则创建，使用追加读写模式
        with open(os.path.join(config.current_directory,config.Log_File), 'a+') as file:
            # 将数据写入文件
            file.write(data)
            file.write("\r\n")

    def check_mail_valid(self, email):
        # 检查收件人
        # to_recipients_list = [recipient.email_address for recipient in email.to_recipients]
        # print(to_recipients_list)
        # print(email.to_recipients)
        # print(email.cc_recipients)

        # if config.MAIL_ACCOUNT not in to_recipients_list: # 开发模式
        #     return False, f"{to_recipients_list} 发件人不包含 {config.MAIL_ACCOUNT}"

        subject = email.subject
        # if ("合同" in subject) == False:
        #     return False, f"邮件主题{subject} 不包含合同"

        if "转发" in subject or "re" in subject.lower():
            return False, f"邮件主题{subject} 包含转发"

        # if "答复" in subject or "re" in subject.lower():
        #     return False, f"邮件主题{subject} 包含答复"

        if "大模型分析" in email.body: # 代表处理过
            return False,f"邮件body{email.body} 包含大模型分析"

        if not email.attachments:
            return False,f"邮件不包含附件"
        return True, ""

    def mail_listen(self):
        # 收取未读邮件
        unread_emails = self.account.inbox.filter(is_read=False)
        accepted_extensions = ['doc', 'docx']

        mail_result = []
        for email in unread_emails:
            # 获取邮件标题和正文内容
            # 获取发件人和发件时间
            b, msg = self.check_mail_valid(email)
            if b == False:
                email.is_read = True
                email.save()
                logger.info(f"skip mail cause: {msg}")
                continue
            filenames = []
            # 检查邮件是否含有附件

            for attachment in email.attachments:
                if len(attachment.name.rsplit('.')) < 2:
                    continue
                # 下载邮件附件
                filename, file_extension = attachment.name.rsplit('.', 1)
                file_extension = file_extension.lower()
                single_data = SingleMailData()
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


    def mail_send_log(self, email,html,attachments=[], to_recipient=[], cc_recipients=[]):
        # Create a message object
        m = Message(account=self.account, subject=f'法务大模型风险分析结果——日志-subject:{email.subject}')

        # Attach the HTML content to the email
        m.body = HTMLBody(html)
        # m.is_html = True  # Specify that the body content is HTML

        # Set the recipient's email address
        m.to_recipients = to_recipient
        m.cc_recipients = cc_recipients
        # Send the email
        # attach files
        for attachment in attachments:
            if attachment is not None:
                with open(attachment, "rb") as f:
                    cont = f.read()
                attchF = FileAttachment(name=os.path.basename(attachment), content=cont)
                m.attach(attchF)
        m.send_and_save()
        logger.info(
            f"Mail Log to_recipient:{[i.email_address for i in to_recipient]}, cc_recipients:{[i.email_address for i in cc_recipients]}")

    def mail_send(self, html,attachments, to_recipient=[], cc_recipients=[]):
        # Create a message object
        m = Message(account=self.account, subject='法务大模型风险分析结果')

        # Attach the HTML content to the email
        m.body = HTMLBody(html)
        # m.is_html = True  # Specify that the body content is HTML

        # Set the recipient's email address
        m.to_recipients = to_recipient
        m.cc_recipients = cc_recipients
        # Send the email
        # attach files
        if attachments is not None:
            with open(attachments, "rb") as f:
                cont = f.read()
            attchF = FileAttachment(name=os.path.basename(attachments), content=cont)
            m.attach(attchF)
        m.send_and_save()
        logger.info(
            f"Mail to_recipient:{[i.email_address for i in to_recipient]}, cc_recipients:{[i.email_address for i in cc_recipients]}")


class DocxProcess():
    def __init__(self, convert_path, template_path, source_txt_path, source_docs_path,diff_docs_path,match_data_list,baichuan_llm, single_mail_data,
                 *args, **kwargs):
        self.source_txt_path = source_txt_path
        self.source_docs_path= source_docs_path
        self.baichuan_llm = baichuan_llm
        self.convert_path = convert_path
        self.diff_docs_path = diff_docs_path
        self.template_path = template_path
        self.single_mail_data = single_mail_data
        self.match_data_list=match_data_list
        create_directory_if_not_exists(self.convert_path)
        create_directory_if_not_exists(self.diff_docs_path)
        create_directory_if_not_exists(self.source_txt_path)
        self.resp={}

    def get_result(self):
        return self.resp

    def single_attachment_handle_process(self):

        yield format_sse_json(status="data",msg='开始处理word文档')
        error=False
        error_str=""


        try:
            # 1. 防止测试使用 已修订的文档  拒绝附件文件 的所有修订
            deny_email_doc_file = word_deny_filename_build(self.single_mail_data.email_doc_file,self.convert_path,"deny_")
            deny_word_revision(path=self.single_mail_data.email_doc_file,save_path=deny_email_doc_file)
            self.single_mail_data.email_doc_file=deny_email_doc_file

            yield format_sse_json('清除上传文件中批注信息')
            txt = docfilename_to_txtfilename(file_path=self.single_mail_data.email_doc_file,base_dir=self.convert_path)
            self.single_mail_data.email_txt_file = txt

            # 2. 第1步拒绝后的email附件 转换 txt 与 text_dct,email_text_mapping
            # text_dict 是 收缩文本:{page,part}
            # email_text_mapping 是 收缩文本:原始文本
            self.single_mail_data.email_text_dict,self.single_mail_data.email_text_mapping = word2txt(
                docpath=self.single_mail_data.email_doc_file, txtpath=self.single_mail_data.email_txt_file)

            yield format_sse_json('检验模板匹配度')
            # 3. 确认附件对应的 模板文件版本，以及是否有效
            record_cls, valid = self.version_valid(self.single_mail_data.email_txt_file)


            if not valid:
                #是否中资
                source_docx,valid,zhongzi_contract = zhongzi_valid_search(self.single_mail_data.email_txt_file)
                if not valid:
                    error_str = "%s %s" % (self.single_mail_data.email_doc_file, "没有匹配到模板")
                    logger.error("%s %s %s" % (self.single_mail_data.email_doc_file, "没有匹配到模板", "==" * 15))

                    raise ContractException(error_str)
                self.single_mail_data.zhongzi=True
                self.single_mail_data.standpoint="0"
                self.single_mail_data.zhongzi_soft= True if zhongzi_contract == "soft" else False
                self.single_mail_data.zhongzi_hard= True if zhongzi_contract == "hard" else False
                # 找到源docx
                self.single_mail_data.src_doc_file = os.path.join(self.source_docs_path,source_docx)
                # 通过源docx 命名源txt
                self.single_mail_data.src_txt_file = os.path.join(self.source_txt_path, (source_docx).replace("docx","txt"))
                self.single_mail_data.src_text_dict,self.single_mail_data.src_text_mapping=word2txt(docpath=self.single_mail_data.src_doc_file, txtpath=self.single_mail_data.src_txt_file)
                # doc 中的table
                self.single_mail_data.word_table_output = word_table_output(self.single_mail_data.email_doc_file)

                diff_docx=os.path.join(self.diff_docs_path,f"{int(time.time())}_diff.docx")
                yield format_sse_json(f'对比模板差异')
                # 对比doc 生成 diff.docx
                create_revisions_docx(self.single_mail_data.src_doc_file,self.single_mail_data.email_doc_file,diff_docx)
                logger.info(f"Create: {diff_docx}")

                # html 与 result_risk 生成
                yield from self.generate_html_txt_diff(single_mail_data=self.single_mail_data)

                if len(self.single_mail_data.result_risk) == 0:
                    text_dict={}
                else:
                    # 根据风险提示 写入diff.docx 批注
                    text_dict=rebuild_page_word_comments_write_with_dict(diff_docx,self.single_mail_data.result_risk)

                html = self.html_generate(single_mail_data=self.single_mail_data,lines=list(text_dict.values()))
                self.resp={'error':error,'error_str':error_str,'diff_docx':os.path.basename(diff_docx),'html':html}
                return html,diff_docx,error,error_str
            else:

                self.single_mail_data.dyx = record_cls.dyx
                self.single_mail_data.reserved = record_cls.reserved
                self.single_mail_data.src_record_cls = record_cls

                # 4. find 模板文件 docx file path
                src_docx_file_list = find_src_version_filename(search_path=self.source_docs_path,
                                                              dyx=record_cls.dyx,
                                                              reserved=record_cls.reserved)
                if len(src_docx_file_list) != 1:
                    logger.error(f"!!!!! src_txt_file_list: {src_docx_file_list} ,len neq 1")
                    error=True
                    raise ContractException(f"src_txt_file_list len gt 1,files: {src_docx_file_list}")

                yield format_sse_json(f'匹配到模板{src_docx_file_list[0]}')
                # 找到源docx
                self.single_mail_data.src_doc_file = os.path.join(self.source_docs_path,src_docx_file_list[0])
                # 通过源docx 命名源txt
                self.single_mail_data.src_txt_file = os.path.join(self.source_txt_path, (src_docx_file_list[0]).replace("docx","txt"))
                # 5. 源docx 转换 txt 与 text_dict,不需要text_mapping
                # text_dict 是 收缩文本:{page,part}

                self.single_mail_data.src_text_dict,self.single_mail_data.src_text_mapping=word2txt(docpath=self.single_mail_data.src_doc_file, txtpath=self.single_mail_data.src_txt_file)


                # logger.info(f"匹配到的 src_txt_file: {self.single_mail_data.src_txt_file} ")

                # xxx 生成html diff.docx
                diff_docx=os.path.join(self.diff_docs_path,f"{int(time.time())}_diff.docx")
                yield format_sse_json(f'对比模板差异')
                # 对比doc 生成 diff.docx
                create_revisions_docx(self.single_mail_data.src_doc_file,self.single_mail_data.email_doc_file,diff_docx)

                # html 与 result_risk 生成
                yield from self.generate_html_txt_diff(single_mail_data=self.single_mail_data)
                if len(self.single_mail_data.result_risk) == 0:
                    text_dict={}
                else:
                    # 根据风险提示 写入diff.docx 批注
                    text_dict=rebuild_page_word_comments_write_with_dict(diff_docx,self.single_mail_data.result_risk)

                html = self.html_generate(single_mail_data=self.single_mail_data,lines=list(text_dict.values()))
                self.resp={'error':error,'error_str':error_str,'diff_docx':os.path.basename(diff_docx),'html':html}
                return html,diff_docx,error,error_str

        except Exception as e:
            error=True
            html = self.generate_html_fail(self.single_mail_data, warnings="附件文件没有匹配到模板文件,请自行审核!")
            # logger.error("!!! Fail: %s " % (e.__str__()))
            error_str=e.__str__()
            traceback.print_exc()
            self.resp = {'error': error, 'error_str': error_str, 'diff_docx': None, 'html': html}
            return html,None,error,error_str


    def version_valid(self, txt):

        record_cls, valid = version_valid_search(txt)


        return record_cls, valid



    def generate_html_fail(self, single_mail_data, **kwargs):
        txt_file_email = single_mail_data.email_txt_file

        # Load the Jinja2 template
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template('template.html')

        # Render the template with the dynamic content
        html_output = template.render(lines=[], src_docx_file="",
                                      email_file=os.path.basename(single_mail_data.email_doc_file), **kwargs)
        #
        # with open('diff_output_custom_parser.html', 'w', encoding='utf-8') as file:
        #     file.write(html_output)
        return html_output


    def valid_skip_row_zhongzi(self, line,type, page, risks_list, skip_page=None, skip_word=None):
        if skip_page is None:
            skip_page = ['1'] if self.single_mail_data.zhongzi_soft else ['1','18']
        row = replace_str(line["line"])
        if page in skip_page:
            logger.info(f"!!!! line code: {type},skip line:{row} ,page:{page} ,cause in skip_page:{skip_page}")
            return True
        if len(row) <= config.MIN_LINE_LEN:
            logger.info(f"!!!! line code: {type},skip line:{row} ,page:{page} ,cause len lte {config.MIN_LINE_LEN}")
            return True

        skip_word_both = [{"include": ["盖章", "甲方："], "exclude": []},
                          {"include":["盖章","乙方："],"exclude":[]},
                          {"include": ["授权代表", "签字"], "exclude": []},
                          {"include": ["日期："], "exclude": []},
                          {"include": ["日期:"], "exclude": []},
                          {"include": ["合同价款","人民币"], "exclude": ["支付"]},
                          {"include": ["大写", "人民币"], "exclude": ["支付"]},
                          ]
        for word in skip_word_both:
            if all_match(word["include"], row) and any_match(word["exclude"], row) == False:
                logger.info(f"!!!! line code: {type},skip line:{row} ,cause in skip both word:{word}")
                return True

        for table in self.single_mail_data.word_table_output.values():
            if row in table:
                logger.info(f"!!!! line code: {type},skip line:{row} ,cause in table:{table}")
                return True
        return False

    def valid_skip_row(self, line,type, page, risks_list, skip_page=None, skip_word=None):
        if skip_page is None:
            skip_page = ['1', '13','14']
        if skip_word is None:
            skip_word = ['盖章', '签字', '联系方式:','概述']

        skip_word_both = [{"include": ["附件", ":", "协议"], "exclude": ["价格", "费用"]},
                          {"include":["网站应用","邮件应用"],"exclude":[]},
                          {"include": ["年", "月","日"], "exclude": []},
                          {"include": ["新闻资讯", "电子商务"], "exclude": []},
                          {"include": ["新闻资讯", "文学小说"], "exclude": []},
                          {"include": ["个人网站", "电子政务"], "exclude": []},
                          {"include":["信息发布","文学小说"],"exclude":[]}]

        must_skip_word= ['盖章', '签字', '联系方式:','概述','网站应用类型:','服务产品类型','带宽产品。',"用户方服务器主要用途:","机柜产品:"]
        symbol = ['、','。','；','：','，','（','）','(',')','【','】','[',']','{','}','<','>','《','》','"','“','”','‘','’','、','/','\\','|','_','——','———','———','——','———','———','———','�']

        row = replace_str(line["line"])

        if len(row) <= config.MIN_LINE_LEN:
            logger.info(f"!!!! line code: {type},skip line:{row} ,page:{page} ,cause len lte {config.MIN_LINE_LEN}")
            return True

        skip_page = skip_page
        skip_word = skip_word
        if page in skip_page:
            logger.info(f"!!!! line code: {type},skip line:{row} ,page:{page} ,cause in skip_page:{skip_page}")
            return True

        for s in symbol:
            if row == s:
                logger.info(f"!!!! line code: {type},skip line:{row} ,cause in symbol:{s}")
                return True

        for s in must_skip_word:
            if row == s:
                logger.info(f"!!!! line code: {type},skip line:{row} ,cause in must_skip_word:{s}")
                return True

        for word in skip_word:
            if row.find(word) != -1:
                logger.info(f"!!!! line code: {type},skip line:{row} ,cause in skip word:{skip_word}")
                return True


        for word in skip_word_both:
            if all_match(word["include"], row) and any_match(word["exclude"], row) == False:
                logger.info(f"!!!! line code: {type},skip line:{replace_str(row)} ,cause in skip both word:{word['include']}")
                return True
        # if len(risks_list) == 0:
        #     logger.info(f"!!!! line code: {line['code']},skip,line:{row} ,cause risks_list len 0")
        #     return True

        return False

    def llm_effect(self, line, key_word_need_valid, **kwargs):
        system_prompt_cot_custom = None
        if key_word_need_valid:
            # 创建 Jinja2 模板对象
            template = Template(cot_template_rule_change)
            # 渲染模板，传递变量
            rendered_output = template.render(kwargs)
            # rendered_output = template.render(examples_terms=examples_terms, risk_warning=risk_warning)
            system_prompt_cot_custom = SystemMessagePromptTemplate.from_template(rendered_output)

        effect = self.baichuan_llm.get_resp(line['code'], line,
                                            system_prompt_cot_custom=system_prompt_cot_custom)
        return effect
    def match_keyword(self,obj,line):
        if obj is not None:
            for match in self.match_data_list:
                if "key_words" in match:
                    key_list=match["key_words"].split(",")
                    if all_match(key_list,line):
                        return match
        return None
    def match_json(self,obj,line):
        if obj is not None:
            for match in self.match_data_list:
                if "match_rule_json" in match:
                    match_dict=ast.literal_eval(match["match_rule_json"])
                    include_and_list=match_dict["include"]["and"]
                    include_or=match_dict["include"]["or"]
                    if any_match(include_or,line) and all_match(include_and_list,line) :
                        return match
        return None
    def match_part(self,obj):
        if obj is not None:
            for match in self.match_data_list:
                if "parts" in match :
                    parts_list=match["parts"].split(",")
                    if len(parts_list) >=1 and obj["part"] in parts_list:
                        return match
        return None
    def match_page(self,obj):
        if obj is not None:
            for match in self.match_data_list:
                if "pages" in match:
                    page_list=match["pages"].split(",")
                    if len(page_list) >=1 and obj["page"] in page_list:
                        return match
        return None
    def risk_match_obj(self,diff_type,line,newline):
        if diff_type.lower() == "change":
            obj=self.single_mail_data.src_text_dict.get(replace_str(line),None)
            # page match
            match_item=self.match_page(obj)
            if match_item is not None:
                return match_item,"page"
            # part match
            match_item=self.match_part(obj)
            if match_item is not None:
                return match_item,"part"
            match_item=self.match_keyword(obj,newline) # change use newline
            if match_item is not None:
                return match_item,"keyword"
            match_item = self.match_json(obj, newline)  # change use newline
            if match_item is not None:
                return match_item,"json"

        if diff_type.lower() == "left" or diff_type.lower() == "right":
            obj=self.single_mail_data.src_text_dict.get(replace_str(line),None)
            # page match
            match_item=self.match_page(obj)
            if match_item is not None:
                return match_item,"part"
            # part match
            match_item=self.match_part(obj)
            if match_item is not None:
                return match_item,"part"
            match_item=self.match_keyword(obj,line) # left use line
            if match_item is not None:
                return match_item,"keyword"
            match_item = self.match_json(obj, line)  # left use line
            if match_item is not None:
                return match_item,"json"

        return None,None

    def llm_with_risk_match(self,diff_type,line,newline=None):
        cot_tpl=""
        if self.single_mail_data.standpoint=="1":
            match_obj,match_type=self.risk_match_obj(diff_type,line,newline)
        else: #中咨
            match_obj,match_type=None,None
        user_tpl=""
        if diff_type.lower() == "change":
            user_tpl=change_tpl_user_prefix %(line,newline)
            if match_obj is None:
                cot_tpl=change_cot_default if self.single_mail_data.standpoint == "1" else change_cot_default_zhongzi
            else:
                cot_tpl=match_obj["change_tpl_cot"]
        if diff_type.lower() == "left":
            user_tpl=left_tpl_user_prefix %(line)
            if match_obj is None:
                cot_tpl=left_cot_default if self.single_mail_data.standpoint == "1" else left_cot_default_zhongzi
            else:
                cot_tpl=match_obj["left_tpl_cot"]

        if diff_type.lower() == "right":
            user_tpl=right_tpl_user_prefix %(line)
            if match_obj is None:
                cot_tpl=right_cot_default if self.single_mail_data.standpoint == "1" else right_cot_default_zhongzi
            else:
                cot_tpl=match_obj["right_tpl_cot"]


        logger.info(f"code: {diff_type}")
        logger.info(f"match_type:{match_type} , match_obj_id:{match_obj['id'] if match_type is not None else None}")
        logger.info(f"cot_tpl:{cot_tpl}")
        logger.info(f"user_tpl:{user_tpl}")
        effect = self.baichuan_llm.get_resp_custom_tpl(DiffCode=diff_type,cot_template=cot_tpl,human_input=user_tpl)
        return effect,match_obj
    def find_parts_priority(self, risk_impact_list):

        for risk_impact in risk_impact_list:
            if risk_impact.parts_priority >= 100:
                return [risk_impact]
        return []

    def find_keywords(self, target_str):
        risk_list = []
        for key, value in risk_keywords_dict.items():
            if key in target_str:
                risk_list.append(value)

        return risk_list

    def find_math_rule_json(self, target_str):
        risk_list = []
        for record in risk_json_record:
            match_rule_json = record.match_rule_json
            exclude = match_rule_json["exclude"]
            exclude_and_rule = exclude["and"]
            exclude_or_rule = exclude["or"]
            # 排除规则不确定

            # and ,or 都为真
            include = match_rule_json["include"]
            include_and_rule = include["and"]
            include_or_rule = include["or"]
            if all_match(include_and_rule, target_str) and any_match(include_or_rule, target_str):
                risk_list.append(record)

        return risk_list

    def find_context(self, target_str):
        target_index = 0
        dest_elm = self.single_mail_data.dest_elm
        # 确定 目标文本的位置
        for i, value in enumerate(dest_elm):
            if replace_str(value.text) == target_str:
                target_index = i
        page = self.single_mail_data.src_record_cls.page_rule(target_index, '')

        part = self.single_mail_data.src_record_cls.part_rule(target_index)
        return page, part

    def merge_risk(self, source_list, risk_list1, risk_list2):
        risks_list = copy.deepcopy(source_list)
        risks_list.extend(risk_list1)
        risks_list.extend(risk_list2)

        risk_set_id = set([v.id for v in risks_list])
        return [v for v in risks_list if v.id in risk_set_id]

    def email_text_mapping_save(self,diff_type,line_copy,newline_copy,line_info):

        # DiffCode.LEFTONLY
        if diff_type == DiffCode.LEFTONLY:
            replace_line_copy = replace_str(line_copy)
            source_text_dict = self.single_mail_data.src_text_mapping[replace_line_copy]
            self.single_mail_data.result_risk.setdefault(source_text_dict, line_info)

        if diff_type == DiffCode.RIGHTONLY:
            replace_line_copy = replace_str(line_copy)
            source_text_dict = self.single_mail_data.email_text_mapping[replace_line_copy]
            self.single_mail_data.result_risk.setdefault(source_text_dict, line_info)

        if diff_type == DiffCode.CHANGED:
            replace_new_line_copy = replace_str(newline_copy)
            source_text_dict = self.single_mail_data.email_text_mapping[replace_new_line_copy]
            self.single_mail_data.result_risk.setdefault(source_text_dict, line_info)


    def generate_html_txt_diff(self, single_mail_data):

        txt_file_std = single_mail_data.src_txt_file
        txt_file_email = single_mail_data.email_txt_file

        with open(txt_file_std, 'r',encoding='utf-8') as file1, open(txt_file_email, 'r',encoding='utf-8') as file2:
            src_content = file1.readlines()
            mail_content = file2.readlines()

        differ_parser = DifflibParser(src_content, mail_content)
        line_number = 0
        lines = []
        total_differ = [line for line in differ_parser if line['code'] > 0]
        # differ = total_differ[0:config.MAX_DIFF_LINE + 1]



        for diff_index, line in enumerate(total_differ):
            if line_number >= config.MAX_DIFF_LINE:
                break
            if line['code'] > 0:
                risk = None
                if str_valid(line["line"]):
                    continue
                effect=""
                line_copy = copy.deepcopy(line["line"])
                newline_copy = ""
                replace_new_line_copy = ""
                line_info = {}
                replace_line_copy = replace_str(line_copy)

                if 'newline' in line:
                    newline_copy = copy.deepcopy(line['newline'])



                if line['code'] == DiffCode.LEFTONLY:
                    try:
                        type = "附件比模板减少的内容"

                        page = self.single_mail_data.src_text_dict[replace_str(line_copy)]["page"]
                        part = self.single_mail_data.src_text_dict[replace_str(line_copy)]["part"]


                        # skip rule
                        if self.single_mail_data.zhongzi:
                            if self.valid_skip_row_zhongzi(line=line,type=type,page=page, risks_list=None):
                                continue
                        else:
                            if self.valid_skip_row(line=line,type=type,page=page, risks_list=None):
                                continue

                        effect, match_obj = self.llm_with_risk_match("left", line_copy)
                        # if match_obj is not None:
                        #     risk = match_obj["risk_warning"]


                        line_number += 1
                        line_info = {
                            'tpl_text': line_copy,
                            'number': line_number,
                            'type': type,
                            'page': page,
                            'part': part,
                            'mail_text': f'<span style="background-color: #ff9999;">{line_copy}</span>',
                            'effect': effect,
                            # 'risk': risk
                        }

                    except Exception as e:
                        logger.error(f"!!! Left Skip ERROR: {e.__str__()}, line:{line}")
                        continue

                elif line['code'] == DiffCode.RIGHTONLY:
                    try:
                        type = "模板中不存在的内容"

                        page=self.single_mail_data.email_text_dict[replace_str(line_copy)].get("page","")
                        part=self.single_mail_data.email_text_dict[replace_str(line_copy)].get("part","")
                        # skip rule
                        if self.single_mail_data.zhongzi:
                            if self.valid_skip_row_zhongzi(line=line,type=type,page=page, risks_list=None):
                                continue
                        else:
                            if self.valid_skip_row(line=line, type=type, page=page, risks_list=None,
                                                   skip_word=['用户方:', '名称:', '盖章', '签字', '联系方式:',
                                                              '纳税人识别号:',
                                                              '注册地址:', '电话:', '地址:', '电子邮件:',
                                                              '北京世纪互联宽带数据中心托管服务协议(']):
                                continue

                        effect,match_obj=self.llm_with_risk_match("right",line_copy)
                        # if match_obj is not None:
                        #     risk=match_obj["risk_warning"]
                        line_number += 1
                        line_info = {
                            'tpl_text': line_copy,
                            'number': line_number,
                            'type': type,
                            'page': page,
                            'part': f"{part}" if len(part) > 0 else part,
                            'mail_text': f'<span style="background-color: #99ff99;">{replace_str(line_copy)}</span>',
                            'effect': effect,
                            # 'risk': risk
                        }

                    except Exception as e:
                        logger.error(f"!!! Right Skip ERROR: {e.__str__()}, line:{line}")
                        continue
                elif line['code'] == DiffCode.CHANGED:
                    type = "模板与附件内容不同"
                    leftchanges = line.get('leftchanges', [])
                    rightchanges = line.get('rightchanges', [])

                    new_line_list = list(newline_copy)
                    line_list = list(line_copy)

                    output_line = copy.deepcopy(line_list)
                    output_newline = copy.deepcopy(new_line_list)

                    for ii in leftchanges:
                        output_line[ii] = f'<span style="background-color: #ff9999;">{line_list[ii]}</span>'

                    for i in rightchanges:
                        output_newline[i] = f'<span style="background-color: #99ff99;">{new_line_list[i]}</span>'

                    try:
                        page = self.single_mail_data.src_text_dict[replace_line_copy]["page"]
                        part = self.single_mail_data.src_text_dict[replace_line_copy]["part"]
                        # skip rule

                        if self.single_mail_data.zhongzi:
                            if self.valid_skip_row_zhongzi(line=line,type=type,page=page, risks_list=None):
                                continue
                        else:
                            if self.valid_skip_row(line=line, type=type, page=page, risks_list=None):
                                continue

                        effect,match_obj=self.llm_with_risk_match("change",line_copy,newline_copy)
                        # if match_obj is not None:
                        #     risk=match_obj["risk_warning"]

                        line_number += 1

                        line_info = {
                            'tpl_text': f'{"".join(output_line)}',
                            'number': line_number,
                            'type': type,
                            'page': page,
                            'part': part,
                            'mail_text': f'{"".join(output_newline)}',
                            'effect': effect,
                            # 'risk': risk
                        }

                    except Exception as e:
                        traceback.print_exc()
                        logger.error(f"!!! change Skip ERROR: {e.__str__()}, line:{line}")
                        continue
                else:
                    # html_output += f'<td>{line["line"]}</td></tr>'
                    continue
                # print(1111,json.dumps(line_info,indent=4,ensure_ascii=False))
                # print(11122221, line_copy)
                yield format_sse_json(status="detail_diff",
                                      msg=json.dumps(line_info,ensure_ascii=False))
                # 保存 批注使用
                self.email_text_mapping_save(line["code"],line_copy,newline_copy,line_info)
                lines.append(line_info)


        return lines
    def html_generate(self,single_mail_data,lines):

        txt_file_std = single_mail_data.src_txt_file
        src_docx_file = (os.path.basename(txt_file_std)).replace(".txt", ".docx")
        # Load the Jinja2 template
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template('template.html')

        # Render the template with the dynamic content
        html_output = template.render(lines=lines[0:config.MAX_DIFF_LINE], src_docx_file=src_docx_file,
                                      email_file=os.path.basename(single_mail_data.email_doc_file),
                                      max_diff_line=config.MAX_DIFF_LINE, total_risk_line_num=len(lines)
                                      )
        logger.info(
            f"config max line:{config.MAX_DIFF_LINE},current risk line info:{len(lines)}")
        #
        # with open('diff_output_custom_parser.html', 'w', encoding='utf-8') as file:
        #     file.write(html_output)
        return html_output



def main():
    # source_docs_path = "/data/work/pydev/word_对比转换/source_docx"
    # source_txt_path = "/data/work/pydev/word_对比转换/source_txt"

    source_docs_path = config.SOURCE_DOCS_PATH
    source_txt_path = config.SOURCE_TXT_PATH
    # 所有 docx 转换txt
    # txt_dict, txt_list = convert_docx_to_txt(src_doc_dir=source_docs_path, txt_dir=source_txt_path)


    from run_init_db import match_data_list

    # if config.RUN_TYPE.lower() == "dev":
    #     logger.info(f"当前配置文件为 {config.RUN_TYPE}")
    #     dev_dir = r"z:\AI_Json\source_docx_modify\dev_files"
    #     for filename in os.listdir(dev_dir):
    #         if '~' not in filename and "docx" in filename and 'deny_' not in filename:
    #             single_data = SingleMailData()
    #             # 如果扩展名在接受的列表中，下载附件
    #             single_data.email_doc_file = os.path.join(dev_dir, filename)
    #             logger.info(f"读取到的待处理文件: {single_data.email_doc_file}")
    #
    #             html, attachments, error = DocxProcess(
    #                                convert_path=config.CONVERT_PATH,
    #                                template_path=config.TEMPLATE_DIR,
    #                                source_txt_path=config.SOURCE_TXT_PATH,
    #                                source_docs_path=config.SOURCE_DOCS_PATH,
    #                                diff_docs_path=config.DIFF_DOCS_PATH,
    #                                single_mail_data=single_data,
    #                                match_data_list=match_data_list,
    #                                baichuan_llm=baichuan_llm(url=baichuan_url,
    #                                                          proxy=config.PROXY)).single_attachment_handle_process()
    #
    #             with open('demo.html', 'w', encoding='utf-8') as file:
    #                 file.write(html)

    # ep = EmailProcess(download_path=config.DOWNLOAD_PATH,
    #              convert_path=config.CONVERT_PATH,
    #              source_txt_path=source_txt_path,
    #              template_path=config.TEMPLATE_DIR,
    #              baichuan_llm=baichuan_llm(url=config.OPENAI_API_BASE, proxy=config.PROXY),
    #              cred_user=config.MAIL_CRED_USER,
    #              cred_pwd=config.MAIL_CRED_PWD,
    #              mail_server=config.MAIL_SERVER,
    #              mail_account=config.MAIL_ACCOUNT
    #              )
    # 创建线程列表
    threads = []

    import threading
    from web_app.main import start_web

    # threads.append(t)

    tt = threading.Thread(target=start_web )
    tt.start()

    # t = threading.Thread(target=ep.handle_process )
    # t.start()
    #
    # t.join()
    tt.join()

# 1. 加上抄送人
# 2. 匹配 不到的模板 要提示
# 3。 显示模板文件名称
if __name__ == "__main__":
    main()
    # threads.append(tt)

    # 等待所有线程结束
    # for t in threads:
    #     t.start()
    #     t.join()