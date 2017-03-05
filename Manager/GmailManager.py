#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import logging
import smtplib
import email
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys
from logging.handlers import RotatingFileHandler

import param
from Repository.FoodRepository import FoodRepository
from Repository.UserRepository import UserRepository


class GmailManager:
    def __init__(self):
        self.food_repo = FoodRepository()
        self.user_repo = UserRepository()
        # create formatter and add it to the handlers
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt="%d/%m/%Y %H:%M:%S")

        # create file handler which logs even debug messages
        my_handler = RotatingFileHandler('gmail.log', mode='a', maxBytes=10 * pow(10, 6),
                                         backupCount=5, encoding=None, delay=0)
        my_handler.setFormatter(formatter)
        my_handler.setLevel(logging.DEBUG)

        # create logger with 'spam_application'
        self.logger = logging.getLogger('gmail')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(my_handler)

    def connect(self):
        # Login to INBOX
        self.logger.info("Connexion au compte Gmail en cours...")
        imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)

        try:
            imap.login(param.gmail['username'], param.gmail['password'])
            return imap
        except:
            self.logger.error("Unexpected error: %s", sys.exc_info()[1])

    def read(self):
        imap = self.connect()
        try:
            self.logger.info("Recherche de nouveaux emails en cours...")
            imap.select()
            result, data = imap.uid('search', None, "UNSEEN")  # search and return uids instead
            uids = data[0].split()

            if len(uids) == 0:
                self.logger.info("Pas de nouveau email.")
                return
            else:
                self.logger.info('Nouveaux emails non lus en attente...')

            foods = self.food_repo.get_foods()
            sender_accept = self.user_repo.get_users_mails()

            for uid in uids:
                result, data = imap.uid('fetch', uid, '(RFC822)')
                raw_email = data[0][1]

                email_message = email.message_from_bytes(raw_email)
                get_from = re.search('<([^>]+)>', email_message['from'], re.IGNORECASE)
                mail_from = get_from if not get_from else get_from.group(1)
                self.logger.info("Nouveau email reçu de `%s`. Traitement en cours...", mail_from)

                if get_from and mail_from in sender_accept:
                    self.logger.info("L'expéditeur `%s` est utilisateur de l'app --> mail accepté...")
                    msg = ''
                    if email_message.is_multipart():
                        for payload in email_message.get_payload():
                            # if payload.is_multipart(): ...
                            msg = payload.get_payload()
                            break
                    else:
                        msg = email_message.get_payload()

                    self.logger.info("Commande reçue: `%s`.", mail_from, msg)

                    if msg.strip().lower() in ['send shopping list', 'send']:
                        self.send(mail_from, foods)
                        pass
        except:
            self.logger.error("Unexpected error: %s", sys.exc_info()[1])
        finally:
            try:
                self.logger.info('Déconnexion du compte en cours...')
                imap.logout()
            except:
                self.logger.error("Unexpected error: %s", sys.exc_info()[1])

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

        self.logger.info("Envoi de la liste des courses à `%s`.", toaddr)
