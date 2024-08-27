import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from google.cloud import storage, bigquery
from google.cloud.bigquery import SourceFormat, SchemaField
from typing import List

def process_dataframe(df):
    df = df.reindex(columns=['date', 'explanation', "media_type", "title", 'url', "copyright"])
    columns_to_process = ['explanation', 'title', 'copyright']
    df[columns_to_process] = df[columns_to_process].replace({
    '\n': ' ',
    '\"': ' ',
    '\r': ' ',
    }, regex=True)
    df = df.astype(str)
    df['date'] = pd.to_datetime(df['date'])

    return df

def process_json_to_csv(input_file:str, output_folder:str):
    """處理 JSON 檔案並儲存為 CSV"""
    #     # 讀取 JSON 檔案
    df = pd.read_json(input_file)
    df = process_dataframe(df)

    # 使用當前日期來創建分區資料夾
    today_str = datetime.now().strftime('%Y-%m-%d')
    partition_folder = os.path.join(output_folder, f'dt={today_str}')
    os.makedirs(partition_folder, exist_ok=True)
    
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%H%M%S')
    # 使用日期範圍來命名CSV檔案
    file_name = f"apod_{start_date}_{end_date}_{timestamp}.csv"
    # 儲存CSV檔案
    output_file = os.path.join(partition_folder, file_name)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"CSV file '{file_name}' created successfully.")


def upload_csvs_to_gcs(bucket_name, source_folder):
    """
    將資料夾中的所有CSV檔案上傳到 Google Cloud Storage 指定分區。

    :param bucket_name: GCS 桶子的名稱
    :param source_folder: 本地資料夾的路徑，其中包含CSV檔案
    """
    client = storage.Client.from_service_account_json('your_key')
    bucket = client.bucket(bucket_name)

    # 使用當前日期來創建分區路徑
    partition_path = 'partition/dt={}/'.format(datetime.now().strftime('%Y-%m-%d'))

    # 遍歷資料夾中的所有CSV檔案
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.csv'):
            local_file_path = os.path.join(source_folder, file_name)
            # 設定 GCS 上的檔案路徑
            gcs_file_path = os.path.join(partition_path, file_name).replace("\\", "/")  # Windows compatibility
            
            # 創建 Blob 物件
            blob = bucket.blob(gcs_file_path)
            # 上傳檔案
            blob.upload_from_filename(local_file_path)
            print(f"File '{local_file_path}' uploaded to '{gcs_file_path}'.")


def load_gcsdata_to_BQ(
        dataset_id: str, 
        table_id: str, 
        uri: str,
        schema: List[SchemaField], 
        source_format: SourceFormat = SourceFormat.CSV,
        skip_leading_rows: int = 1,
):
    client = bigquery.Client.from_service_account_json('your_key')
    job_config = bigquery.LoadJobConfig(
        source_format = source_format,
        skip_leading_rows = skip_leading_rows,
        schema = schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Overwrite the table or create it if it does not exist
    )
    
    
    load_job = client.load_table_from_uri(
        uri,
        f'{dataset_id}.{table_id}',
        job_config = job_config
)
    load_job.result()
    print("Data loaded into BigQuery table.")

    #     # Generate ID column
    # query = f"""
    # CREATE OR REPLACE TABLE {dataset_id}.{table_id}_with_id AS
    # SELECT
    #     ROW_NUMBER() OVER() AS id,
    #     *
    # FROM
    #     {dataset_id}.{table_id};
    # """
    
    # query_job = client.query(query)
    # query_job.result()  # Wait for the query to finish

    # print("Table with ID column created.")

