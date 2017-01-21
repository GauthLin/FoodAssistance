import imaplib
import smtplib
import email
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import param
from Repository.FoodRepository import FoodRepository
from Repository.UserRepository import UserRepository


class GmailManager:
    def __init__(self):
        self.food_repo = FoodRepository()
        self.user_repo = UserRepository()
        # Login to INBOX
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.imap.login(param.gmail['username'], param.gmail['password'])

    def read(self):
        self.imap.select()
        result, data = self.imap.uid('search', None, "UNSEEN")  # search and return uids instead
        uids = data[0].split()

        foods = self.food_repo.get_foods()
        sender_accept = self.user_repo.get_users_mails()

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

                if msg.strip().lower() in ['send shopping list', 'send']:
                    self.send(mail_from, foods)
                    pass

    def send(self, to, foods):
        fromaddr = param.gmail['username']
        toaddr = to

        msg = MIMEMultipart('alternative')
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Liste de courses"

        html = '<div style="max-width:700px; background-color:#f5f5f5; margin:auto;">' \
               '<div style="font-size: 1.5em;color: whitesmoke;padding: 20px;text-align: center;background-color: #187718;">' \
               'FoodAssistance' \
               '</div>' \
               '<div style="padding: 15px;color: #272727;">' \
               '<p>Bonjour,</p>' \
               '<p>Vous trouverez ci-dessous votre liste des courses :</p><ul>'

        for food in foods:
            quantity = str(food.quantity) if food.quantity and float(food.quantity) > 0 else ''
            html += '<li>%s %s <strong>%s</strong></li>' % (quantity, str(food.measuring_units), food.name)

        html += '</ul>' \
                '</div>' \
                '<div style="font-size: 0.85em;color: whitesmoke;padding: 5px 15px;text-align: center;background-color: #2d3271;">' \
                'Ce message vous a été envoyé automatiquement, merci de ne pas y répondre. ' \
                'Votre réponse ne sera pas traitée ! <br> Nous vous invitons à ajouter l\'adresse mail ' \
                'linard.food.assistance@gmail.com à votre carnet d\'adresses. Ainsi, vous serez sûr(e) de ' \
                'recevoir nos mails.</div>' \
                '</div>'

        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, param.gmail['password'])
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
