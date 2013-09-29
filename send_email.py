#-*-coding:utf-8-*-

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ACCOUNT, EMAIL_PWD, EMAIL_HOST, EMAIL_PORT

logger = logging.getLogger(__name__)

def send_file_via_email(to_email, attachment_file):
    msg = MIMEMultipart()
    msg['from'] = EMAIL_ACCOUNT
    msg['to'] = to_email
    msg['subject'] = 'Convert'

    logger.info('going to send %s to %s from %s', attachment_file, msg['to'],
            msg['from'])

    with open(attachment_file, 'rb') as fp:
        data = fp.read()

    att = MIMEText(data, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(attachment_file)
    msg.attach(att)

    mail = smtplib.SMTP(timeout = 60)

    mail.connect(EMAIL_HOST, EMAIL_PORT)
    mail.ehlo()
    mail.starttls() 

    mail.login(EMAIL_ACCOUNT, EMAIL_PWD)

    logger.info('mail server connected...start sending')
    mail.sendmail(msg['from'], msg['to'], msg.as_string())
    logger.info('email sent')
    mail.close()

if __name__ == '__main__':
    send_file_via_email('wonderfuly@gmail.com', 'decrypt.py')
