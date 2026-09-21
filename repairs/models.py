from django.db import models
from django.conf import settings
from django.db.models import Q

# Using settings.AUTH_USER_MODEL instead of directly importing User
User = settings.AUTH_USER_MODEL

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RepairRequestQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.role == "customer":
            return self.filter(user=user)
        elif user.role in ["technician", "admin"]:
            return self.all()
        else:
            return self.none()


class RepairRequest(models.Model):
    
    SUBMITTED = "submitted"
    INPROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (SUBMITTED, 'Submitted'),
        (INPROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repair_requests')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='repair_requests')
    address = models.CharField(max_length=500, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField()
    objects = RepairRequestQuerySet.as_manager()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_date"]),
        ]
        ordering = ['-created_date']    