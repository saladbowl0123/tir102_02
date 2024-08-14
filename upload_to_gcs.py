import requests
import json
import mimetypes
from google.cloud import storage

# gcs bukect name
bucket_name = 'tir102_apod'

# 讓python 連上gcs
storage_client = storage.Client()

def upload_to_gcs(url, date, bucket_name):
    res = requests.get(url)
    content = res.content
    
    # 取名
    filename = f"{date}.jpg"
    
    # 自動辨識內容的類型，mime_type, encoding
    mime_type, _ = mimetypes.guess_type(filename)
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    
    # 將內容上傳至gcs 並指定MIME類型
    blob.upload_from_string(content, content_type=mime_type)
    print(f"File uploaded to {filename} in bucket {bucket_name}.")

# 讀取
with open('crawler.json', 'r') as file:
    data = json.load(file)
for item in data:
    upload_to_gcs(item['url'], item['date'], bucket_name)


"""

在本機設置環境變數
export GOOGLE_APPLICATION_CREDENTIALS="/usr/local/key/evans-class-c67887cf1aed.json"

or 
在code裡添加
from google.cloud import storage
storage_client = storage.Client.from_service_account_json('/path/to/your/service-account-file.json')
"""
