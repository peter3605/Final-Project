from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from . import config
import flask_app


def generate_confirmation_token(email):
    serial = URLSafeTimedSerializer('Thisisasecret!')
    return serial.dumps(email, salt='email_confirm')


def confirm_token(token, expiration=3600):
    serial = URLSafeTimedSerializer('Thisisasecret!')
    try:
        email = serial.loads(
            token,
            salt='email_confirm',
            max_age=expiration
        )
        print("HI IM TAKING AN L")
    except SignatureExpired:
        return False
    return email
