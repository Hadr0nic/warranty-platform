import boto3
from django.conf import settings
import uuid
import os

def upload_to_arvan(file_obj, folder="uploads"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    ext = os.path.splitext(file_obj.name)[1]
    filename = f"{folder}/{uuid.uuid4()}{ext}"

    s3.upload_fileobj(
        file_obj,
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        ExtraArgs={
            "ContentType": file_obj.content_type,
            "ACL": "public-read",  # or remove if private
        }
    )

    return f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{filename}"
