import pandas as pd
import re


def get_comets():

    # 網頁 URL
    url = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/cometfact.html"

    # 使用 pandas 讀取網頁中的表格
    tables = pd.read_html(url)

    # 檢視抓取到的表格數量
    print(f"抓取到的表格數量: {len(tables)}")

    # 只想要第一個表格
    df = tables[0]

    # 解除 MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns]

    # 去除欄位名稱中的連字符
    df.columns = df.columns.str.replace('-', '')

    # 去除最後一個 '_'
    df.columns = [re.sub(r'_([^_]*)$', r'\1', col) for col in df.columns]


    #第一列設為欄位名稱
    #df.columns = df.iloc[0]
    #df = df[1:]  # 刪除第一列

    # # 處理欄位名稱中的 NaN 值
    # df.columns = df.columns.fillna("Unnamed")

    # # 檢查欄位名稱的唯一性，並將重複的 "Unnamed" 欄位名稱重新命名
    # df.columns = [f"{col}_{i+1}" if col == "Unnamed" else col for i, col in enumerate(df.columns)]


    # 檢視表格內容
    print(df)
    print(df.columns)
    print(type(df.columns))

    return df

df = get_comets()