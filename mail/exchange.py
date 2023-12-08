from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

class exchange_demo():

    def __init__(self):
        self.cred = Credentials(r'21VIANET\tao.jun', 'Taojun!@#')
        self.config = Configuration(server='mail.21vianet.com', credentials=self.cred, auth_type=NTLM)

        self.account = Account(
            primary_smtp_address='tao.jun@neolink.com', config=self.config, autodiscover=False, access_type=DELEGATE
        )
    def mail_send(self,to_recipient=[], cc_recipients=[]):
        # 收取未读邮件
        m = Message(account=self.account, subject='HTML Email Test',body="tttttt")

        # Attach the HTML content to the email

        # m.is_html = True  # Specify that the body content is HTML

        # Set the recipient's email address
        m.to_recipients = to_recipient
        m.cc_recipients = cc_recipients
        # Send the email
        m.send_and_save()


if __name__== "__main__":
    ed=exchange_demo()
    html_content=ed.mail_send(to_recipient=['tao.jun@neolink.com'],cc_recipients=['61566027@163.com','tao.jun@neolink.com'])

