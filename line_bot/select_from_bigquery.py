from google.cloud import bigquery
import pandas as pd

BQ_PROJECT = 'my-project-tir102-bigquery'
BQ_DB = 'tir102_apod'
BQ_TABLE_PLANET = 'Planet'
BQ_TABLE_CONSTELLATION = 'Constellation'
BQ_TABLE_APOD = 'apod'
BQ_TABLE_TAGS = 'tags'
COLUMN_NAME_NAME = 'NAME'
COLUMN_NAME_PLANET_ID = 'Planet_ID'
COLUMN_NAME_CONSTELLATION_NAME = 'Constellation_Name'
COLUMN_NAME_START_DATE = 'Start_date'
COLUMN_NAME_DATE = 'date'

client = bigquery.Client()

def query(query):
    return client.query(query).result()

# RowIterator.to_dataframe() uses too much memory:
# https://github.com/googleapis/google-cloud-python/issues/7293

def query_planet_names():
    query_planet_names_data = f"""
        SELECT {COLUMN_NAME_NAME}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_PLANET}
        ORDER BY {COLUMN_NAME_PLANET_ID};
    """

    rows = query(query_planet_names_data)

    data = [list(row)[0].title() for row in rows]

    return data

def query_constellation_names():
    query_constellation_names_data = f"""
        SELECT {COLUMN_NAME_CONSTELLATION_NAME}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_CONSTELLATION}
        ORDER BY {COLUMN_NAME_START_DATE};
    """

    rows = query(query_constellation_names_data)

    data = [list(row)[0].title() for row in rows]

    return data

def query_apod(date_str):
    query_apod_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_APOD}
        WHERE {COLUMN_NAME_DATE} = '{date_str}';
    """

    rows = query(query_apod_data)

    data = [list(row) for row in rows]
    columns = [field.name for field in rows.schema]
    df = pd.DataFrame(data=data, columns=columns)

    return df
