#!/usr/bin/env python

import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import mimetypes

class SendMime:
    def __init__(self, attachment, from_adr, to_adr, mail_serv, msg_body = None, subject='<Default subject>',mail_port=587, trace=2):
        self.attachment = attachment
        self.from_adr = from_adr
        self.to_adr = to_adr
        self.msg_body = msg_body
        self.subject = subject
        self.mail_serv = mail_serv
        self.mail_port = mail_port
        self.trace = trace

    def send_smtp(self,msg):
        s = smtplib.SMTP(self.mail_serv)
        try:
            if self.trace > 0: s.set_debuglevel(1)
            s.sendmail(self.from_adr, self.to_adr, msg)
        except smtplib.SMTPException:
            print ('Send mail error...')
        finally:
	        s.quit()

    def mime_send_attach(self):
        m = MIMEMultipart()
        m['Subject'] = self.subject
        ctype, encoding = mimetypes.guess_type(self.attachment)
        maintype, subtype = ctype.split('/')
        m.attach(MIMEText(self.msg_body))
        fp = open(self.attachment, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename='report.pdf')
        m.attach(msg)
        self.send_smtp(m.as_string())



if __name__=='__main__':
    mail_serv = 'maildomen.ru'
    from_adr = 'some_report_server@test.ru'
    to_adr = ['login1@test.ru','#LOGINGROUP@test.ru']
    from_header = 'From: {}\r\n'.format(from_adr)
    to_header = 'To: {}\r\n\r\n'.format(to_adr)
    subj = 'Subj: sending PDF file'
    attach = '/tmp/hw.pdf'
    msg_body = '''
        This is letter text with pdf attach
        '''
    msg = '{}\n{}\n{}\n'.format(from_header, to_header, msg_body)
    send_mail = SendMime(attach,from_adr,to_adr,mail_serv, msg,subj, trace=0)
    send_mail.mime_send_attach()
