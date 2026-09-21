from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from accounts.models import User

class PermissionErrorNotification(Exception):
    pass


# notifications/services.py
from .tasks import send_email_task
from accounts.models import User
from django.conf import settings

def notify_admins_new_comment(comment):
    recipients = User.objects.filter(
        role__in=["technician", "admin"]
    ).exclude(email="")

    for user in recipients:
        send_email_task.delay(
            user_id=user.id,
            comment_id=comment.id,
            template_html="notifications/email/new_comment.html",
            template_txt="notifications/email/new_comment.txt",
        )