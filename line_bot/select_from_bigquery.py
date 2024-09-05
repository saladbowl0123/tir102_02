from google.cloud import bigquery
import pandas as pd

BQ_PROJECT = 'my-project-tir102-bigquery'
BQ_DB = 'tir102_apod'
BQ_TABLE_APOD = 'apod'
BQ_TABLE_TAGS = 'tags'
COLUMN_NAME_DATE = 'date'

client = bigquery.Client()

def query(query):
    return client.query(query).result()

def query_apod(date_str):
    query_apod_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_APOD}
        WHERE {COLUMN_NAME_DATE} = '{date_str}';
    """

    rows = query(query_apod_data)

    # RowIterator.to_dataframe() uses too much memory:
    # https://github.com/googleapis/google-cloud-python/issues/7293
    data = [list(row) for row in rows]
    columns = [field.name for field in rows.schema]
    df = pd.DataFrame(data=data, columns=columns)

    return df
