import imaplib
import smtplib
import email
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import param


class GmailManager:
    def __init__(self):
        # Login to INBOX
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.imap.login(param.gmail['username'], param.gmail['password'])

    def read(self, foods, sender_accept):
        self.imap.select()
        result, data = self.imap.uid('search', None, "UNSEEN")  # search and return uids instead
        uids = data[0].split()

        for uid in uids:
            result, data = self.imap.uid('fetch', uid, '(RFC822)')
            raw_email = data[0][1]

            email_message = email.message_from_bytes(raw_email)
            get_from = re.search('<([^>]+)>', email_message['from'], re.IGNORECASE)
            mail_from = get_from if not get_from else get_from.group(1)

            if get_from and mail_from in sender_accept:
                msg = ''
                if email_message.is_multipart():
                    for payload in email_message.get_payload():
                        # if payload.is_multipart(): ...
                        msg = payload.get_payload()
                        break
                else:
                    msg = email_message.get_payload()

                if msg.strip().lower() == 'send shopping list':
                    self.send(mail_from, foods)
                    pass

    def send(self, to, foods):
        fromaddr = param.gmail['username']
        toaddr = to

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Liste de courses"

        body = "Bonjour, \r\n\r\n"
        body += "Vous trouverez ci-dessous la liste des courses : \r\n"

        for food in foods:
            body += '- %s %s %s \r\n' % (str(food.quantity), str(food.measuring_units), food.name)

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "FoodAssistanceNoel2016")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
