from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import User
from comments.models import Comment
from .services import PermissionErrorNotification

@shared_task(bind=True, max_retries=3)
def send_email_task(self, user_id, comment_id, template_html, template_txt):
    try:
        user = User.objects.get(id=user_id)
        comment = Comment.objects.select_related(
            "user", "repair_request"
        ).get(id=comment_id)

        if user.role not in ["technician", "admin"]:
            raise PermissionErrorNotification("User not allowed to receive emails.")

        subject = f"New comment on repair: {comment.repair_request.title}"

        context = {
            "recipient": user,
            "comment": comment,
            "commenter": comment.user,
            "repair": comment.repair_request,
            "site_name": settings.SITE_NAME,
        }

        html_body = render_to_string(template_html, context)
        text_body = render_to_string(template_txt, context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)

        return f"Email sent to {user.email}"

    except Exception as exc:
        raise self.retry(exc=exc)
