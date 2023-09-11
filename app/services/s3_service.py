from flask import current_app
from app.extensions import s3_client

def upload_file_to_s3(file, bucket_name, s3_file_name):
    s3Client = s3_client()
    try:
        current_app.logger.info(f"Uploading {s3_file_name} to {bucket_name}")
        s3Client.upload_fileobj(
            file,
            bucket_name,
            s3_file_name
        )
        current_app.logger.info("Upload successful")
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return False
    return True