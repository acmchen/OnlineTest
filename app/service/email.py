from flask_mail import Message
from app.extensions import mail
from app.settings import DevelopmentConfig
from itsdangerous import URLSafeTimedSerializer as UrlSerializer

def send_email(subject,sender,recipients,html):
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=[recipients]
    )
    msg.html = html
    mail.send(msg)

def generate_email_token(email):
    s = UrlSerializer(DevelopmentConfig.SECRET_KEY)
    return s.dumps({'email': email})

def verify_email_token(token, expiration=600):
    s = UrlSerializer(DevelopmentConfig.SECRET_KEY)
    try:
        email = s.loads(token, max_age=expiration)
    except:
        return None
    return email
