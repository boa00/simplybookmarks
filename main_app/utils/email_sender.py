import os
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_gmail_session() -> smtplib.SMTP:
    try:
        session = smtplib.SMTP('smtp.gmail.com', port=587)
        session.starttls()
        session.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASSWORD"])
    except:
        print('Something went wrong')    
    return session

def generate_email(mail_reciever: str, mail_subject: str, mail_content: str) -> MIMEMultipart:
    message = MIMEMultipart('alternative')
    message['From'] = os.environ["EMAIL_USER"]
    message['To'] = mail_reciever
    message['Subject'] = mail_subject
    message.attach(MIMEText(mail_content, 'html'))
    return message

def generate_reset_password_content(jwt_token: str) -> str:
    url = f"http://localhost:3000/reset_password/forms/{jwt_token}"
    content = " To update password, go to the following page: <br>" + url + "<br><br> If you accedentally recieved this message, please, ignore it"
    return content

def send_reset_password_email(jwt_token: str, reciever: str) -> None:
    session = generate_gmail_session()
    content = generate_reset_password_content(jwt_token=jwt_token)
    email_message = generate_email(
        mail_reciever=reciever, 
        mail_subject="Simplybookmarks reset password", 
        mail_content=content
    ).as_string()
    session.sendmail(from_addr=os.environ["EMAIL_USER"], to_addrs=reciever, msg=email_message)
