from google.cloud import storage
from google.oauth2 import service_account
from datetime import timedelta

credentials = service_account.Credentials.from_service_account_file('service_account_key.json')

def generate_signed_url(bucket_name, blob_name, credentials, expiration_minutes=15):
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes))

    return url
