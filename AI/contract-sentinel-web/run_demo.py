import copy
import logging
import time
from jinja2 import Environment, FileSystemLoader
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import os
from unstructured.partition.docx import partition_docx
from jinja2 import Template
import Config
from service.文本匹配段落 import WordDocumentParser
from service.utils import replace_str, str_valid,  create_directory_if_not_exists, find_closest_value,any_match,all_match
from exchangelib.protocol import close_connections
from typing import Type
import urllib3

urllib3.disable_warnings()
from pytz import timezone
import sys
from run_init_db import word_2_record,risk_impact
from pydiff_gui.difflibparser.difflibparser import DiffCode, DifflibParser
from service.确定版本 import base_valid, sjhl_valid, preset_valid, find_src_version_filename, dyx_valid, ele2lines, \
    convert_docx_to_txt,ele2txt,version_valid_by_elem
from service.file_struct_define import dyx_unstd_reserved, undyx_unstd_reserved, dyx_unstd_unreserved, \
    undyx_unstd_unreserved
from sqlalchemy import create_engine

from service.llm import *

from config import BaseConfig as config
from service.g import logger, ContractException,risk_keywords_dict,risk_json_record
from service.db import loadSession,session




# 此句用来消除ssl证书错误，exchange使用自签证书需加上
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter


# 中国时区
# china_tz = timezone('Asia/Shanghai')


class SingleMailData:
    src_txt_file = ""
    src_record_cls = object
    # src_doc_file = ""
    dyx = False
    reserved = False
    email_txt_file = ""
    email_doc_file = ""

    dest_unstruct_dict = {}

    dest_unstruct_elm = {}
    dest_elm = object


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
        self.cred = Credentials(r'21VIANET\tao.jun', r'Taojun!@#')
        self.config = Configuration(server='mail.21vianet.com', credentials=self.cred, auth_type=NTLM)
        self.account = Account(
            primary_smtp_address='tao.jun@neolink.com', config=self.config, autodiscover=False, access_type=DELEGATE
        )

    def handle_process(self):
        while 1 == 1:

            try:
                mail_result = self.mail_listen()
            except Exception as e:
                logger.error(f"!!!!!! mail_listen Fail,check Cred,account")
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

                self.attachments_handle_process(mail)

                logger.info("===" * 40)
            time.sleep(60)

    def attachments_handle_process(self, mail: dict):
        email = mail["mail"]
        filenames = mail["filenames"]
        for index, single_mail_data in enumerate(filenames):
            logger.info("%s %s %s" % ("==" * 15, "第%s个附件开始处理" % (index + 1), "==" * 15))

            html = DocxProcess(download_path=self.download_path,
                               convert_path=self.convert_path,
                               template_path=self.template_path,
                               source_txt_path=self.source_txt_path,
                               single_mail_data=single_mail_data,
                               baichuan_llm=self.baichuan_llm).single_attachment_handle_process()

            if email.cc_recipients is None:
                email.cc_recipients = []

            recipient_mailbox = Mailbox(email_address='tao.jun@neolink.com', name='tao.jun')
            email.cc_recipients.append(recipient_mailbox)
            self.mail_send(html=html, to_recipient=[email.sender], cc_recipients=email.cc_recipients)
            logger.info("%s %s %s" % ("==" * 15, "第%s个附件处理结束" % (index + 1), "==" * 15))

    def check_mail_valid(self,email):
        # 检查收件人
        to_recipients_list=[recipient.email_address for recipient in email.to_recipients]
        if config.MAIL_ACCOUNT not in to_recipients_list:
            return False,f"{to_recipients_list} 发件人不包含 {config.MAIL_ACCOUNT}"

        subject=email.subject
        if "转发" in subject or "re" in subject.lower():
            return False,f"邮件主题{subject} 包含转发"

        return True,""


    def mail_listen(self):
        # 收取未读邮件
        unread_emails = self.account.inbox.filter(is_read=False)
        accepted_extensions = ['doc', 'docx']

        mail_result = []
        for email in unread_emails:
            # 获取邮件标题和正文内容
            # 获取发件人和发件时间
            b,m = self.check_mail_valid(email)
            if b == False:
                logger.info(f"skip mail cause: {m}")
                continue
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

    def mail_send(self, html, to_recipient=[], cc_recipients=[]):
        # Create a message object
        m = Message(account=self.account, subject='HTML Email Test')

        # Attach the HTML content to the email
        m.body = HTMLBody(html)
        # m.is_html = True  # Specify that the body content is HTML

        # Set the recipient's email address
        m.to_recipients = to_recipient
        m.cc_recipients = cc_recipients
        # Send the email
        m.send_and_save()
        logger.info(
            f"Mail to_recipient:{[i.email_address for i in to_recipient]}, cc_recipients:{[i.email_address for i in cc_recipients]}")


class DocxProcess():
    def __init__(self, download_path, convert_path, template_path, source_txt_path, baichuan_llm, single_mail_data, *args, **kwargs):
        self.download_path = download_path
        self.source_txt_path = source_txt_path
        self.baichuan_llm = baichuan_llm
        self.convert_path = convert_path
        self.template_path = template_path
        self.single_mail_data=single_mail_data

    def single_attachment_handle_process(self,):
        try:
            # email附件 转换 dict  elements
            self.unstruct_process(single_mail_data=self.single_mail_data)

            # 确认附件中的 模板版本
            record_cls, valid = self.version_valid(self.single_mail_data.dest_elm)

            # email附件 转换 txt
            txt = self.Docx2txt(file_path=self.single_mail_data.email_doc_file, mail_ele=self.single_mail_data.dest_elm)
            self.single_mail_data.email_txt_file = txt


            if not valid:
                logger.error("%s %s %s" % (self.single_mail_data.email_doc_file, "没有匹配到模板", "==" * 15))
                raise ContractException("%s %s" % (self.single_mail_data.email_doc_file, "没有匹配到模板"))

            else:
                self.single_mail_data.dyx = record_cls.dyx
                self.single_mail_data.reserved = record_cls.reserved
                self.single_mail_data.src_record_cls= record_cls
                # find txt file path
                src_txt_file_list = find_src_version_filename(source_txt_path=self.source_txt_path,
                                                              dyx=record_cls.dyx,
                                                              reserved=record_cls.reserved)
                if len(src_txt_file_list) != 1:
                    logger.error(f"!!!!! src_txt_file_list: {src_txt_file_list} ,len neq 1")
                    raise ContractException(f"src_txt_file_list len gt 1,files: {src_txt_file_list}")

                self.single_mail_data.src_txt_file = os.path.join(self.source_txt_path, src_txt_file_list[0])
                logger.info(f"匹配到的 src_txt_file: {self.single_mail_data.src_txt_file} ")
                # xxx 生成html
                html = self.generate_html_txt_diff(single_mail_data=self.single_mail_data)

        except Exception as e:
            html = self.generate_html_fail(self.single_mail_data, warnings="附件文件没有匹配到模板文件,请自行审核!")
            logger.error("!!! Fail: %s " % (e.__str__()))

        return html

    def version_valid(self, ele):
        # file_content = ele2lines(elements=ele)
        valid = False
        record_cls = object
        record_cls,elements=version_valid_by_elem(ele)
        if len(elements)>0:
            valid=True


        return record_cls, valid

    def unstruct_process(self, single_mail_data):
        # elements = partition_docx(filename=single_mail_data.src_doc_file)
        elements1 = partition_docx(filename=single_mail_data.email_doc_file)
        single_mail_data.dest_elm = elements1

        for index, value in enumerate(elements1):
            single_mail_data.dest_unstruct_dict[replace_str(value.text)] = {"id": value.id,
                                                                            "parent_id": value.metadata.parent_id,
                                                                            "line": index,
                                                                            "page_number": value.metadata.page_number}
            single_mail_data.dest_unstruct_elm[value.id] = value.text

    def Docx2txt(self, file_path, mail_ele):
        file_name = os.path.basename(file_path)  # Gets the file name with extension
        file_name_list = os.path.splitext(file_name)  # Gets the file extension
        file_ext = file_name_list[1]
        file_name_real = file_name_list[0]
        out_file = os.path.join(self.convert_path, file_name_real + ".txt")
        # with open(out_file, 'w', encoding='utf-8') as outfile:
        #     doc = docx2txt.process(file_path)
        #     outfile.write(doc)
        ele2txt(mail_ele,out_file,source_record_cls=None)
        # with open(out_file, "w") as f:
        #     for i in mail_ele:
        #         real_txt = replace_str(i.text)
        #         if len(real_txt) == 0:
        #             # print(f"skip element {i}")
        #             continue
        #         f.write(real_txt)
        #         f.write("\n")
        return out_file

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

    def valid_skip_row(self, line, page, risks_list, skip_page=None, skip_word=None):
        if skip_page is None:
            skip_page = ['1', '13']
        if skip_word is None:
            skip_word = ['盖章', '签字', '联系方式:']

        skip_word_both= [{"include":["附件",":","协议"],"exclude":["价格","费用"]}]

        row = replace_str(line["line"])
        skip_page = skip_page
        skip_word = skip_word
        if page in skip_page:
            logger.debug(f"!!!! line code: {line['code']},skip line:{row} ,page:{page} ,cause in skip_page:{skip_page}")
            return True

        for word in skip_word:
            if row.find(word) != -1:
                logger.debug(f"!!!! line code: {line['code']},skip line:{row} ,cause in skip word:{skip_word}")
                return True

        for word in skip_word_both:
            if all_match(word["include"],row) and any_match(word["exclude"],row)==False:
                logger.debug(f"!!!! line code: {line['code']},skip line:{row} ,cause in skip both word:{word}")
                return True
        # if len(risks_list) == 0:
        #     logger.debug(f"!!!! line code: {line['code']},skip,line:{row} ,cause risks_list len 0")
        #     return True

        return False


    def llm_effect(self,line,key_word_need_valid,**kwargs):
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

    def find_parts_priority(self,risk_impact_list):

        for risk_impact in risk_impact_list:
            if risk_impact.parts_priority >=100:
                return [risk_impact]
        return []

    def find_keywords(self,target_str):
        risk_list=[]
        for key,value in risk_keywords_dict.items():
            if key in target_str:
                risk_list.append(value)

        return risk_list
    
    def find_math_rule_json(self,target_str):
        risk_list=[]
        for record in risk_json_record:
            match_rule_json=record.match_rule_json
            exclude=match_rule_json["exclude"]
            exclude_and_rule=exclude["and"]
            exclude_or_rule=exclude["or"]
            # 排除规则不确定

            # and ,or 都为真
            include=match_rule_json["include"]
            include_and_rule=include["and"]
            include_or_rule=include["or"]
            if all_match(include_and_rule,target_str) and any_match(include_or_rule,target_str):
                risk_list.append(record)

        return risk_list

    def find_context(self,target_str):
        target_index=0
        dest_elm=self.single_mail_data.dest_elm
        # 确定 目标文本的位置
        for i, value in enumerate(dest_elm):
            if replace_str(value.text) == target_str:
                target_index=i
        page=self.single_mail_data.src_record_cls.page_rule(target_index,'')

        part=self.single_mail_data.src_record_cls.part_rule(target_index)
        return page,part

    def merge_risk(self,source_list,risk_list1,risk_list2):
        risks_list=copy.deepcopy(source_list)
        risks_list.extend(risk_list1)
        risks_list.extend(risk_list2)

        risk_set_id=set([v.id for v in risks_list])
        return [v for v in risks_list if v.id in risk_set_id]

    def generate_html_txt_diff(self, single_mail_data):

        txt_file_std = single_mail_data.src_txt_file
        txt_file_email = single_mail_data.email_txt_file

        with open(txt_file_std, 'r') as file1, open(txt_file_email, 'r') as file2:
            src_content = file1.readlines()
            mail_content = file2.readlines()

        differ_parser = DifflibParser(src_content, mail_content)
        line_number = 0
        lines = []
        total_differ = [line for line in differ_parser if line['code'] > 0]
        # differ = total_differ[0:config.MAX_DIFF_LINE + 1]

        for diff_index, line in enumerate(total_differ):
            if line['code'] > 0:
                part = ""
                page = ""
                tpl_text = ""
                effect = ""
                risk = ""
                tpl_text_record_all = []
                tpl_text_record = object
                if str_valid(line["line"]):
                    continue

                if line['code'] == DiffCode.LEFTONLY:
                    row=line['line']
                    type = "附件比模板减少的内容"
                    key_word_need_valid=False
                    examples_terms=""
                    risk_warning=""
                    tpl_text_record_all = session.query(word_2_record).filter(word_2_record.dyx == single_mail_data.dyx,
                                                                              word_2_record.reserved == single_mail_data.reserved,
                                                                              word_2_record.content.like(
                                                                                  f'%{replace_str(row)}%')).all()
                    try:

                        if len(tpl_text_record_all) == 1:
                            tpl_text_record = tpl_text_record_all[0]

                        # 如果 文本内容在 模板中有多条 一样的，找距离最近的
                        if len(tpl_text_record_all) > 1:
                            related_list = [i.line for i in tpl_text_record_all]
                            closest_value, closest_index = find_closest_value(diff_index, related_list)
                            tpl_text_record = tpl_text_record_all[closest_index]

                        if len(tpl_text_record_all) == 0:
                            raise ContractException(f"tpl_text_record len 0")

                        page = tpl_text_record.page_number
                        part = tpl_text_record.part
                        risks_list = tpl_text_record.risk_impact


                    except Exception as e:
                        logger.error(f"!!! left Skip ERROR: {e.__str__()}, line:{line}")
                        continue

                    if self.valid_skip_row(line, page, risks_list):
                        continue


                    if len(risks_list) > 0:
                        key_word_need_valid = True
                        examples_terms = risks_list[0].examples_terms
                        risk_warning = risks_list[0].risk_warning

                    line_number += 1

                    risk = "\n".join([v.risk_warning for v in risks_list if v.focus.find("left") != -1])
                    # context = tpl_text_record[0].content
                    # result = single_mail_data.src_docparse.find_paragraph_by_text(target_text=replace_str(line["line"]))
                    # context=result['section_info']

                    if part != "":

                        # logger.info("left 大模型QA: %s" % replace_str(human_input))
                        # effect = self.baichuan_llm.get_resp(DiffCode.LEFTONLY, human_input)
                        effect=self.llm_effect(line=line,key_word_need_valid=key_word_need_valid,examples_terms=examples_terms,risk_warning=risk_warning)

                    line_info = {
                        'tpl_text': row,
                        'number': line_number,
                        'type': type,
                        'page': page,
                        'part': part,
                        'mail_text': f'<span style="background-color: #ff9999;">{row}</span>',
                        'effect': effect,
                        'risk': risk
                    }

                elif line['code'] == DiffCode.RIGHTONLY:
                    row=line['line']
                    type = "模板中不存在的内容"
                    key_word_need_valid=False
                    examples_terms=""
                    risk_warning=""
                    # xxx 找到与源文件最近的文本 确定段落与页数
                    page,part = self.find_context( target_str=replace_str(row))

                    # 搜索 key_word 包含一个就算
                    risks_list_keywords=self.find_keywords(target_str=replace_str(row))
                    
                    # 搜索 math_json_rule 包含一个就算
                    risks_list_math_rule=self.find_math_rule_json(target_str=replace_str(row))

                    risks_list = self.merge_risk([],risks_list_keywords,risks_list_math_rule)

                    if self.valid_skip_row(line, page, risks_list,skip_word = ['用户方:','名称:','盖章', '签字', '联系方式:','纳税人识别号:','注册地址:','电话:','地址:','电子邮件:','北京世纪互联宽带数据中心托管服务协议(']):
                        continue



                    if len(risks_list) > 0:
                        key_word_need_valid = True
                        examples_terms = risks_list[0].examples_terms
                        risk_warning = risks_list[0].risk_warning

                    line_number += 1
                    risk = "\n".join([v.risk_warning for v in risks_list if v.focus.find("right") != -1])

                    if part != "":

                        # logger.info("right,大模型QA: [%s]" % replace_str(human_input))
                        # effect = self.baichuan_llm.get_resp(DiffCode.RIGHTONLY, human_input)
                        effect=self.llm_effect(line=line,key_word_need_valid=key_word_need_valid,examples_terms=examples_terms,risk_warning=risk_warning)

                    line_info = {
                        'tpl_text': tpl_text,
                        'number': line_number,
                        'type': type,
                        'page': page,
                        'part': f"在{part}后面" if len(part) > 0 else part ,
                        'mail_text': f'<span style="background-color: #99ff99;">{replace_str(row)}</span>',
                        'effect': effect,
                        'risk': risk
                    }

                elif line['code'] == DiffCode.CHANGED:
                    row=line['line']
                    type = "模板与附件内容不同"
                    leftchanges = line.get('leftchanges', [])
                    rightchanges = line.get('rightchanges', [])
                    # new_line = list(line['newline'])
                    new_line_list = list(line['newline'])
                    line_list = list(line['line'])
                    output_line = copy.deepcopy(line_list)
                    output_newline = copy.deepcopy(new_line_list)
                    # Highlight individual different characters in red and green
                    # for i in range(len(line_list)):
                    for ii in leftchanges:
                        output_line[ii] = f'<span style="background-color: #ff9999;">{line_list[ii]}</span>'

                    for i in rightchanges:
                        output_newline[i] = f'<span style="background-color: #99ff99;">{new_line_list[i]}</span>'
                    try:
                        tpl_text_record_all = session.query(word_2_record).filter(
                            word_2_record.dyx == single_mail_data.dyx,
                            word_2_record.reserved == single_mail_data.reserved,
                            word_2_record.content.like(f'%{replace_str(row)}%')).all()

                        if len(tpl_text_record_all) == 1:
                            tpl_text_record = tpl_text_record_all[0]

                        # 找到 邮件中附件文件的行 与 模板文件  哪行比较近
                        if len(tpl_text_record_all) > 1:
                            related_list = [i.line for i in tpl_text_record_all]
                            closest_value, closest_index = find_closest_value(diff_index, related_list)
                            tpl_text_record = tpl_text_record_all[closest_index]

                        if len(tpl_text_record_all) == 0:
                            raise ContractException(f"tpl_text_record len 0")

                        page = tpl_text_record.page_number
                        part = tpl_text_record.part


                    except Exception as e:
                        logger.error(f"!!! change Skip ERROR: {e.__str__()}, line:{line}")
                        continue

                    risks_list=self.find_parts_priority(tpl_text_record.risk_impact)

                    key_word_need_valid=False
                    examples_terms=""
                    risk_warning=""
                    if len(risks_list) > 0:
                        risks_list = risks_list
                        logger.info(f"find_parts_priority:100 {risks_list[0]}")
                    else:
                        risks_list = []
                        # 搜索 key_word 包含一个就算
                        risks_list_keywords = self.find_keywords(target_str=replace_str(line["newline"]))
                        # 搜索 key_word 包含一个就算
                        risks_list_math_rule = self.find_math_rule_json(target_str=replace_str(line["newline"]))

                        # risks_list_keywords,risks_list_math_rule可能有重复
                        risks_list=self.merge_risk(risks_list, risks_list_keywords,risks_list_math_rule)

                        if len(risks_list) > 0:
                            key_word_need_valid = True
                            examples_terms = risks_list[0].examples_terms
                            risk_warning= risks_list[0].risk_warning

                    if self.valid_skip_row(line, page, risks_list):
                        continue

                    line_number += 1


                    risk = "\n".join([v.risk_warning for v in risks_list if v.focus.find("change") != -1])

                    # context = tpl_text_record[0].content
                    # result = single_mail_data.dest_docparse.find_paragraph_by_text(target_text=replace_str(line["newline"]))
                    # context=result['section_info']
                    if part != "":
                        effect=self.llm_effect(line=line,key_word_need_valid=key_word_need_valid,examples_terms=examples_terms,risk_warning=risk_warning)
                        # human_input = f"""
                        # 原条款:{replace_str(line["line"])}
                        # 修改过条款:{replace_str(line["newline"])}"""
                        # logger.info("change 大模型QA: %s" % replace_str(human_input))
                        # system_prompt_cot_custom=None
                        # if key_word_need_valid:
                        #     # 创建 Jinja2 模板对象
                        #     template = Template(cot_template_rule_change)
                        #     # 渲染模板，传递变量
                        #     rendered_output = template.render(examples_terms=examples_terms,risk_warning=risk_warning)
                        #     system_prompt_cot_custom = SystemMessagePromptTemplate.from_template(rendered_output)
                        #
                        #
                        # effect = self.baichuan_llm.get_resp(DiffCode.CHANGED, human_input,system_prompt_cot_custom=system_prompt_cot_custom)
                    line_info = {
                        'tpl_text': f'{"".join(output_line)}',
                        'number': line_number,
                        'type': type,
                        'page': page,
                        'part': part,
                        'mail_text': f'{"".join(output_newline)}',
                        'effect': effect,
                        'risk': risk
                    }


                else:
                    # html_output += f'<td>{line["line"]}</td></tr>'
                    continue

                lines.append(line_info)
        src_docx_file = (os.path.basename(txt_file_std).split("_", 3))[3].replace(".txt", ".docx")
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


# 1. 加上抄送人
# 2. 匹配 不到的模板 要提示
# 3。 显示模板文件名称
if __name__ == "__main__":
    # source_docs_path = "/data/work/pydev/word_对比转换/source_docx"
    # source_txt_path = "/data/work/pydev/word_对比转换/source_txt"

    source_docs_path = config.SOURCE_DOCS_PATH
    source_txt_path = config.SOURCE_TXT_PATH
    # 所有 docx 转换txt
    txt_dict, txt_list = convert_docx_to_txt(src_doc_dir=source_docs_path, txt_dir=source_txt_path)
    # baichuan_url="http://120.133.83.145:8000/v1"
    baichuan_url = config.OPENAI_API_BASE

    os.environ.setdefault("http_proxy", config.PROXY)
    os.environ.setdefault("HTTP_PROXY", config.PROXY)

    if config.RUN_TYPE.lower() == "dev":
        dev_dir="/mnt/AI_Json/source_docx_modify"
        for filename in os.listdir(dev_dir):
            if '~' not in filename and "docx" in filename:
                single_data = SingleMailData()
                # 如果扩展名在接受的列表中，下载附件

                single_data.email_doc_file = os.path.join(dev_dir, filename)

                html = DocxProcess(download_path=config.DOWNLOAD_PATH,
                                   convert_path=config.CONVERT_PATH,
                                   template_path=config.TEMPLATE_DIR,
                                   source_txt_path=config.SOURCE_TXT_PATH,
                                   single_mail_data=single_data,
                                   baichuan_llm=baichuan_llm(url=baichuan_url,
                                                             proxy=config.PROXY)).single_attachment_handle_process()
                with open('demo.html', 'w', encoding='utf-8') as file:
                    file.write(html)


    # EmailProcess(download_path=config.DOWNLOAD_PATH,
    #              convert_path=config.CONVERT_PATH,
    #              source_txt_path=source_txt_path,
    #              template_path=config.TEMPLATE_DIR,
    #              baichuan_llm=baichuan_llm(url=baichuan_url, proxy=config.PROXY),
    #              cred_user=config.MAIL_CRED_USER,
    #              cred_pwd=config.MAIL_CRED_PWD,
    #              mail_server=config.MAIL_SERVER,
    #              mail_account=config.MAIL_ACCOUNT
    #              ).handle_process()
