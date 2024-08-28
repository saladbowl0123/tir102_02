#pip install google-cloud-storage
import os
import json
import requests
from google.cloud import storage
from google.oauth2 import service_account

project_id = 'my-project-tir102'
key_file_path = r"C:\Users\T14 Gen 3\Downloads\bigquery-romona.json"
bucket_name='upload_to_gcs_test'
json_file_name = 'apod_data_2000-01-01_2000-06-30.json'

# 設置認證
credentials = service_account.Credentials.from_service_account_file(key_file_path)

# 創建storage客戶端
storage_client = storage.Client(credentials=credentials, project=project_id)

# 指定bucket名稱
bucket = storage_client.bucket(bucket_name)

# 指定要上傳的本地檔案路徑和檔案名稱
directory = "data"
file_path = os.path.join(directory, json_file_name)

# 讀取內容
with open(file_path,'r') as file:
    pictures = json.load(file)
    for i,item in enumerate(pictures):
        print(f"Index: {i}")
        print(item['date'])
        url = item['url']
        filename = f"{item['date']}"
        media_type = item['media_type']

        if media_type == 'video':
            filename += '.txt'
            content = f"Video URL: {url}"
            mime_type = 'text/plain'
        
        elif media_type =='image':
            try:
                res = requests.get(url)
                content = res.content
                filename += '.jpg'
                mime_type = 'image/jpeg'

                if res.status_code != 200:
                    raise Exception(f"Failed to download content from URL: {url}")
            except Exception as e:
                print(f"Failed to handle URL {item['date']},{url}: {e}")
                continue

        #創建儲存桶裡面的物件
        blob = bucket.blob(filename)
        try:
            blob.upload_from_string(content, content_type=mime_type)
            print(f"File uploaded to {filename} in bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to upload {filename} to bucket {bucket_name}: {e}")
