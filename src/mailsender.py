import smtplib
import email.utils
import os
import csv
import email.Message
from email import Charset
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import quopri

import jinja2

class MailSender(object):

    def __init__(self, toName, toAddr, ticketID):
        # Sender information
        self.fromName = 'Example Example'
        self.fromAddr = 'example@example.com'
        # Receiver/s information
        self.toName = toName
        self.toAddr = []
        self.toAddr.append(toAddr)

        # Support for multiple targets from csv file, no comma

        #with open('testlist.csv', 'rb') as mysecondfile:
        #self.csvdata = csv.reader(mysecondfile, delimiter=' ', quotechar='|')
        #for row in csvdata:
        #receivers.append(row)



        self.ticketID = ticketID

        # Subject of mail
        self.subject = 'Ticket ' + self.ticketID + ' successfully purchased.'

        # Variables to HTML template
        self.context = {
            'name' : toName,
            'qr_code' : ticketID
            }

        self.msg = MIMEMultipart('mixed')
        self.inline = MIMEMultipart ('alternative')

        # Local SMTP - server - Requires working one e.g Postfix
        self.server = smtplib.SMTP('127.0.0.1', 25)
        # Global charset to UTF-8
        Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')

    def createHeaders(self):

        self.msg['To'] = email.utils.formataddr((self.toName, self.toAddr))
        self.msg['From'] = email.utils.formataddr((self.fromName, self.fromAddr))
        self.msg['Subject'] = self.subject
        self.msg['List-Unsubscribe'] = '<mailto:example@example.com>, <example@example.com>'
        self.msg['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'


    def createMessage (self):

        #TXT version of mail
        self.createHeaders()
        with open ('data.txt', 'rb') as mytxt:
            self.text = mytxt.read()

        # HTML version of mail, generated from template
        self.html = self.render('templates/mailtemplate.html', self.context)

        # Mime - parts
        part1 = MIMEText(self.text, 'plain', 'utf-8')
        part2 = MIMEText(self.html, 'html', 'utf-8')

        # Attach to the HTML/TXT version of the mail
        self.inline.attach(part1)
        self.inline.attach(part2)

        # Attach to whole message
        self.msg.attach(self.inline)

    def render(self, tpl_path, context):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(context)

    def sendMail(self):
        self.server.set_debuglevel(True)
        try:
            self.server.sendmail(self.fromAddr, self.toAddr, self.msg.as_string())
        finally:
            self.server.quit()
