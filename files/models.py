from django.db import models
from django.conf import settings
from repairs.models import RepairRequest

from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile


User = settings.AUTH_USER_MODEL


class UploadedFile(models.Model):
    IMAGE = 'image'
    DOCUMENT = 'document'

    TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (DOCUMENT, 'Document'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )

    repair_request = models.ForeignKey(
        RepairRequest,
        on_delete=models.CASCADE,
        related_name='files'
    )

    file_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=IMAGE
    )

    #file_url = models.URLField()
    file = models.FileField(upload_to="repairs/", null=True, blank=True)
    file_url = models.URLField(null=True, blank=True)



    is_minified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_type} for Repair #{self.repair_request.id}"


    def save(self, *args, **kwargs):
        """
        Override save to minify image if is_minified is True.
        """

        if self.is_minified and self.file and self.file_type == self.IMAGE:
            # Openning
            img = Image.open(self.file)
            img_format = img.format

            # Reduce size/quality
            img_io = BytesIO()
            img = img.convert("RGB")  # compatibility
            img.save(img_io, format=img_format, optimize=True, quality=60)

            # Replace file with minified version
            new_name = os.path.basename(self.file.name)
            self.file.save(new_name, ContentFile(img_io.getvalue()), save=False)

        super().save(*args, **kwargs)