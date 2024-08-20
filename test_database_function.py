import pymysql
import pandas as pd

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


