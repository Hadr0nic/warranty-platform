from django.core import signing
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


TOKEN_SALT = "login-token"


def generate_signed_login_token(user, purpose="login"):
    payload = {
        "user_id": user.id,
        "purpose": purpose,
        "ts": timezone.now().timestamp(),
    }
    return signing.dumps(payload, salt=TOKEN_SALT)



def send_email_token(user, purpose="login"):
    token = generate_signed_login_token(user, purpose)

    url = f"{settings.SITE_URL}/accounts/token-login/{token}/"

    send_mail(
        subject="Your FG Warranty login link",
        message=f"Click here to login:\n{url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


import hashlib
from .utils import send_sms_via_smsir

SMS_CODE_LENGTH = 6


def token_to_sms_code(token: str) -> str:
    """
    convert a signed token to a 6-digit SMS code.
    """
    digest = hashlib.sha256(token.encode()).hexdigest()
    return digest[:SMS_CODE_LENGTH].upper()


def send_sms_token(user, phone_number, purpose="login"):
    token = generate_signed_login_token(user, purpose)
    code = token_to_sms_code(token)

    parameters = [
        {"name": "code", "value": code},
    ]

    send_sms_via_smsir(
        mobile=phone_number,
        template_id=settings.SMSIR_TEMPLATE_ID,
        parameters=parameters,
        api_key=settings.SMSIR_API_KEY,
    )

    return token



PASSWORD_RESET_SALT = "password-reset"

def generate_password_reset_token(user):
    payload = {
        "user_id": user.id,
        "ts": timezone.now().timestamp(),
    }
    return signing.dumps(payload, salt=PASSWORD_RESET_SALT)


def send_password_reset_email(user):
    token = generate_password_reset_token(user)
    url = f"{settings.SITE_URL}/accounts/reset-password/{token}/"
    send_mail(
        subject="Reset your FG Warranty password",
        message=f"Click this link to reset your password:\n{url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
