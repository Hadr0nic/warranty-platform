from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    EMAIL = 'email'
    SMS = 'sms'

    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'

    TYPE_CHOICES = [
        (EMAIL, 'Email'),
        (SMS, 'SMS'),
    ]

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
        (FAILED, 'Failed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    notif_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=EMAIL
    )

    notif_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    created_date = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.notif_type})"


from notifications.models import Notification

def send_notification(user, title, message, notif_type="email"):
    if user.role not in ["technician", "admin"]:
        raise PermissionError("You are not allowed to send notifications.")
    
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notif_type=notif_type
    )
        