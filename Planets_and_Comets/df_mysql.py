import pandas as pd
from sqlalchemy import create_engine
from get_comets import get_comets

# pip install cryptography



#planets_df = get_planets()
planets_df = get_comets()


# 建立 MySQL 資料庫連接
username = "root"
password = "12345678"
database_name = "tir102g2"
engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost:3306/{database_name}")

# 將 DataFrame 寫入 MySQL 資料庫中的表
# table_name = "planets"
table_name = "comets"
planets_df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print("DataFrame 已成功寫入 MySQL 資料庫！")
