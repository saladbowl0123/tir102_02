#pip install pandas-gbq 先安裝gbq套件

import pandas as pd
from google.cloud import bigquery
# 創建一個 BigQuery 客戶端
client = bigquery.Client.from_service_account_json("your_key_path")

# 創建一個 DataFrame
data = {
    'column1': ['value1', 'value2'],
    'column2': [10, 20]
}
df = pd.DataFrame(data)

# 設置資料表名 (格式: `project_id.dataset_id.table_id`)
#表格不存在時會自動建立
table_id = 'my-project-tir102-bigquery.tir102_apod.Measurement'

# 將 DataFrame 寫入 BigQuery
df.to_gbq(destination_table=table_id,
          project_id='my-project-tir102-bigquery',
          if_exists='replace')  # 或 'append' 根據需要選擇

#destination_table 表格名稱
#project_id 專案名稱
#if_exists 'replace' 會替換現有表格，'append' 會追加到現有表格。