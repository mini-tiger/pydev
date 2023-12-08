from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

class exchange_demo():

    def __init__(self):
        self.cred = Credentials(r'21VIANET\tao.jun', 'Taojun!@#')
        self.config = Configuration(server='mail.21vianet.com', credentials=self.cred, auth_type=NTLM)

        self.account = Account(
            primary_smtp_address='tao.jun@neolink.com', config=self.config, autodiscover=False, access_type=DELEGATE
        )
    def mail_listen(self):
        # 收取未读邮件
        messages = self.account.inbox.filter(is_read=False).order_by('-datetime_received')
        accepted_extensions = ['doc', 'docx']

        mail_result = []

        for message in messages:
            print(f'Subject: {message.subject}')
            print(f'From: {message.sender}')
            # print(f'To: {message.to}')
            # print(f'CC: {message.cc}')
            # print(f'Sent Time: {message.datetime_sent}')
            # print(f'Received Time: {message.datetime_received}')
            # print('Body:')
            # print(message.body)
            print('-' * 50)
            return message.body

from bs4 import BeautifulSoup

def find_element_by_id(html_content, target_text):
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找包含指定文本的元素
    # element = soup.find('body', string=lambda text: text and target_text in text)
    if soup.text.find(target_text) != -1:
        return "ok"
    else:
        return "false"

if __name__== "__main__":
    ed=exchange_demo()
    html_content=ed.mail_listen()
    print(html_content)
    # 调用函数，传入 HTML 文件路径和要查找的元素 ID
    print(find_element_by_id(html_content, 'hidden'))
