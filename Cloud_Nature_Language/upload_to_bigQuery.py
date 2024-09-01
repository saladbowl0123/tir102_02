#pip install pandas-gbq google-cloud-bigquery

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq 
from entity_to_tags import entity_to_tags


df = pd.read_json(r"C:\Users\T14 Gen 3\Documents\apod-api\data_apod_3years\apod_data_2014-01-01_2016-12-31.json")  
df_combined = entity_to_tags(df)

#認證
key_file_path = r"C:\Users\T14 Gen 3\Downloads\bigquery-romona.json"
credentials = service_account.Credentials.from_service_account_file(key_file_path)

# 建立 BigQuery 客戶端
client = bigquery.Client(credentials=credentials, project='my-project-tir102-bigquery')

# 設定目標資料集和表格名稱
table_id = 'my-project-tir102-bigquery.tir102_apod.tags'

# 手動定義模式
schema = [
    bigquery.SchemaField("date", "DATE"),
    bigquery.SchemaField("tags_en", "STRING"),
    bigquery.SchemaField("tags_zhTW", "STRING"),
]

# 設定 job 的配置
job_config = bigquery.LoadJobConfig(
    schema=schema,  
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND  # WRITE_APPEND/WRITE_TRUNCATE
)

# 將 DataFrame 寫入 BigQuery
job = client.load_table_from_dataframe(df_combined, table_id, job_config=job_config)
job.result()

print(f"已將 {df_combined.shape[0]} 列數據成功寫入 BigQuery")

