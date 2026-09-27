import uuid

import boto3
from flask import current_app


def _s3():
    return boto3.client("s3", region_name=current_app.config["AWS_REGION"])


def upload_report(patient_id, file_storage):
    key = f"reports/{patient_id}/{uuid.uuid4()}-{file_storage.filename}"
    _s3().upload_fileobj(file_storage, current_app.config["S3_BUCKET"], key)
    return key
