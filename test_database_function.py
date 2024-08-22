import pymysql
import pandas as pd
from sqlalchemy import create_engine


def get_connection(host='localhost', port=3306, user='root', passwd='password', charset='utf8mb4'):
    """建立並返回連線"""
    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset=charset)
        print('Successfully connected!')
        return conn
    except pymysql.MySQLError as e:
        print(f"Failed to connect to database: {e}")
        return None


def create_database(conn, database_name):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        conn.commit()
        print(f"Database '{database_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create database '{database_name}': {e}")


def create_table(conn, database_name, table_name, columns):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f'USE {database_name}')
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
            {columns})
        '''
            cursor.execute(create_table_query)
        conn.commit()
        print(f"Table {table_name} created successfully in {database_name}.")
    except Exception as e:
        print(f"Failed to create table '{table_name}': {e}")

#一次創建多個表格
# 定義多個表格的 SQL 語法
# tables_sql = {
#     'table1': '''
#         CREATE TABLE IF NOT EXISTS `table1` (
#             `id` INT AUTO_INCREMENT PRIMARY KEY,
#             `name` VARCHAR(255) NOT NULL,
#             `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     ''',
#     'table2': '''
#         CREATE TABLE IF NOT EXISTS `table2` (
#             `id` INT AUTO_INCREMENT PRIMARY KEY,
#             `description` TEXT,
#             `price` DECIMAL(10, 2) NOT NULL
#         )
#     ''',
#     'table3': '''
#         CREATE TABLE IF NOT EXISTS `table3` (
#             `id` INT AUTO_INCREMENT PRIMARY KEY,
#             `user_id` INT,
#             `order_date` DATE,
#             `amount` DECIMAL(10, 2) NOT NULL
#         )
#     '''
# }

# for table_name, sql in tables_sql.items():
#     create_table(conn, 'test_db', sql)
    
#  關閉連線
#  conn.close()


def insertdata(df, table_name, engine, if_exists='append', index=False):
    """
    將 DataFrame 插入到指定的資料庫表格中。
    :param df: pandas DataFrame 待插入的數據。
    :param table_name: str 目標表格的名稱。
    :param engine: SQLAlchemy Engine 對象，用於連接資料庫。
    :param if_exists: str 當表格已存在時的操作方式，預設為 'append'。可選值：'fail', 'replace', 'append'。
    :param index: bool 是否將 DataFrame 的索引列寫入資料庫，預設為 False。
    """

    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=index)
        print(f"Data added successfully")
    except Exception as e:
        print(f"Data addition failed : {e}")

