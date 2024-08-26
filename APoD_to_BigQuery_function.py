import pandas as pd
from pathlib import Path
import os
from datetime import datetime

def process_dataframe(df):
    df = df.drop(['hdurl','service_version'], axis= 1)
    columns_to_process = ['explanation', 'title', 'copyright']
    df[columns_to_process] = df[columns_to_process].replace({
    '\n': ' ',
    '\"': ''
    }, regex=True)
    df = df.astype(str)
    df['date'] = pd.to_datetime(df['date'])
    df.dtypes

    return df


def process_json_to_csv(input_file:str, output_folder:str):
    """處理 JSON 檔案並儲存為 CSV"""
         # 讀取 JSON 檔案
    df = pd.read_json(input_file)
    df = process_dataframe(df)

    # 使用當前日期來創建分區資料夾
    today_str = datetime.now().strftime('%Y-%m-%d')
    partition_folder = os.path.join(output_folder, f'dt={today_str}')
    os.makedirs(partition_folder, exist_ok=True)
    
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%H%M%S')
    # 使用日期範圍與建立時間來命名CSV檔案
    file_name = f"apod_data_{start_date}_{end_date}_{timestamp}.csv"
    # 儲存CSV檔案
    output_file = os.path.join(partition_folder, file_name)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"CSV file '{file_name}' created successfully.")


