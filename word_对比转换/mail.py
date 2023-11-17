from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import requests
requests.packages.urllib3.disable_warnings()
from pytz import timezone
#此句用来消除ssl证书错误，exchange使用自签证书需加上
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

# 输入你的域账号如example\leo
cred = Credentials(r'21VIANET\tao.jun', 'Taojun!@#')

config = Configuration(server='mail.21vianet.com', credentials=cred, auth_type=NTLM)

account = Account(
    primary_smtp_address='tao.jun@neolink.com', config=config, autodiscover=False, access_type=DELEGATE
)
# 收取未读邮件
unread_emails = account.inbox.filter(is_read=False)
accepted_extensions = ['doc', 'docx', 'pdf', 'xls', 'xlsx']
# 中国时区
china_tz = timezone('Asia/Shanghai')
for email in unread_emails:
    # 获取邮件标题和正文内容
    # 获取发件人和发件时间

    print(f"Sender: {email.sender}")
    print(f"Sent Time: {email.datetime_sent.astimezone(china_tz)}")

    print(f"Subject: {email.subject}")
    print(f"Body: {email.text_body}")
    # 检查邮件是否含有附件
    if not email.attachments:
        print(f"No attachments in email with subject: {email.subject}")

    else:
        for attachment in email.attachments:

            # 下载邮件附件
            filename, file_extension = attachment.name.rsplit('.', 1)
            file_extension = file_extension.lower()

            # 如果扩展名在接受的列表中，下载附件
            if file_extension in accepted_extensions:
                print(f"download {attachment.name}")
                with open(attachment.name, 'wb') as f:
                    f.write(attachment.content)

        # 标记邮件为已读
        email.is_read = True
        email.save()

