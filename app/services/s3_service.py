from flask import current_app
from ..extensions import s3_client

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

def download_from_s3(bucket_name, file_key, download_path):
    s3 = s3_client()
    try:
        s3.download_file(bucket_name, file_key, download_path)
        print(f"Sucessfully downloaded {file_key} to {download_path}.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    