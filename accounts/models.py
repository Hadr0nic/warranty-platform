from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CUSTOMER = "customer"
    TECHNICIAN = "technician"
    ADMIN = "admin"
    ADMIN0 = "messenger admin"

    ROLE_CHOICES = [
        (CUSTOMER, "Customer"),
        (TECHNICIAN, "Technician"),
        (ADMIN, "Admin"),
        (ADMIN0, "messenger admin"),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
    )

    is_verified = models.BooleanField(default=False)

    google_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


