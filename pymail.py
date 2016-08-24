import smtplib
from email.mime.text import MIMEText


def initialize(p_email_address, p_email_pass):
    global email_address, email_pass
    email_address = p_email_address
    email_pass = p_email_pass


def send_mail(body, subject, is_html = False, to_list = []):
    global email_address, email_pass
    if is_html:
        msg = MIMEText(body,'html')
    else:
        msg = MIMEText(body,'plain')
    msg['Subject'] = subject
    mail_raspi = email_address
    msg['From'] = mail_raspi
    msg['To'] = ','.join(to_list)
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(mail_raspi, email_pass)
    for to in to_list:
        mailserver.sendmail(mail_raspi, to, msg.as_string())
    mailserver.quit()
