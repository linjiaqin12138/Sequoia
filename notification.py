import requests
import json
import logging
from requests.auth import HTTPBasicAuth
import settings
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import time
import atexit

email_sender = None

class EmailMgmt:
    def __init__(self, email_config):
        self.message_queue = []
        settings.init()
        self.sender = email_config['sender']
        self.passcode = email_config['passcode']
        self.target = email_config['target']
        self.host = email_config['host']
        self.port = email_config['port']
    def send(self):
        logging.debug('before exist, send the email', self.message_queue)
        email_msg = MIMEText('\n'.join(self.message_queue), 'plain','utf-8')
        email_msg["Subject"] = Header('股票推送', 'utf-8')
        email_msg["From"] = self.sender
        email_msg["To"] = self.target
        self.smtp = SMTP_SSL(self.host, self.port)
        self.smtp.login(self.sender, self.passcode)
        self.smtp.sendmail(self.sender, self.target, email_msg.as_string())
        self.smtp.quit()
    def send_pending(self, msg):
        self.message_queue.append(msg)

        
def push(msg):
    payload = json.dumps({
        "type": "headline",
        "from": settings.config['push']['admin'],
        "to": settings.config['push']['user'],
        "subject": "investing",
        "body": msg
    })
    response = requests.post(settings.config['push']['url'], auth=HTTPBasicAuth(settings.config['push']['admin'],
                                            settings.config['push']['admin_pass']), data=payload)
    print(response.text)
        
def mail(msg):
    global email_sender
    if email_sender is None:
        email_sender = EmailMgmt(settings.config['email'])
        atexit.register(email_sender.send)
    email_sender.send_pending(msg)

def send(msg):
    if settings.config['push']['enable']:
        push(msg)
    if settings.config['email']['enable']:
        mail(msg)
    logging.info(msg)

def statistics(msg=None):
    send(msg)


def strategy(msg=None):
    if msg is None or not msg:
        msg = '今日没有符合条件的股票'
    send(msg)
