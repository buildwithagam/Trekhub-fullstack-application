import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, html_body):
    smtp_host = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', 587))
    smtp_user = os.environ.get('MAIL_USERNAME', '')
    smtp_pass = os.environ.get('MAIL_PASSWORD', '')
    sender = os.environ.get('MAIL_SENDER', smtp_user)

    if not smtp_user or not smtp_pass:
        print(f"[MAIL SKIPPED – set MAIL_USERNAME & MAIL_PASSWORD env vars to enable real sending]")
        print(f"  TO: {to_email}")
        print(f"  SUBJECT: {subject}")
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender, to_email, msg.as_string())
        print(f"[MAIL SENT] To: {to_email} | Subject: {subject}")
        return True
    except Exception as e:
        print(f"[MAIL ERROR] {to_email}: {e}")
        return False
