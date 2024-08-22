import pandas as pd


def get_planets():

    # 網頁 URL
    url = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/"

    # 使用 pandas 讀取網頁中的表格
    tables = pd.read_html(url)

    # 檢視抓取到的表格數量
    print(f"抓取到的表格數量: {len(tables)}")

    # 只想要第一個表格
    df = tables[0]

    # 表格翻轉
    df = df.transpose()

    #第一列設為欄位名稱
    df.columns = df.iloc[0]
    df = df[1:]  # 刪除第一列

    # 處理欄位名稱中的 NaN 值
    df.columns = df.columns.fillna("Unnamed")

    # 檢查欄位名稱的唯一性，並將重複的 "Unnamed" 欄位名稱重新命名
    df.columns = [f"{col}_{i+1}" if col == "Unnamed" else col for i, col in enumerate(df.columns)]


    # 檢視表格內容
    print(df)

    return df

# df = get_planets()