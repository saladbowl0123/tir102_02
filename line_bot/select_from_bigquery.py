from google.cloud import bigquery
import pandas as pd

BQ_PROJECT = 'my-project-tir102-bigquery'
BQ_DB = 'tir102_apod'
BQ_TABLE_PLANET = 'Planet'
BQ_TABLE_CONSTELLATION = 'Constellation'
BQ_TABLE_COMET = 'Comet'
BQ_TABLE_SHOWER = 'Showers2024'
BQ_TABLE_SUN = 'SUN'
BQ_TABLE_APOD = 'apod'
BQ_TABLE_TAGS = 'tags'
COLUMN_NAME_ENGLISH_TAGS = 'tags_en'
COLUMN_NAME_NAME = 'NAME'
COLUMN_NAME_PLANET_ID = 'Planet_ID'
COLUMN_NAME_CONSTELLATION_NAME = 'Constellation_Name'
COLUMN_NAME_COMET_ID = 'Comet_ID'
COLUMN_NAME_SHOWER = 'Shower'
COLUMN_NAME_START_DATE = 'Start_date'
COLUMN_NAME_DATE = 'date'

client = bigquery.Client()

def query(query):
    return client.query(query).result()

# RowIterator.to_dataframe() uses too much memory:
# https://github.com/googleapis/google-cloud-python/issues/7293

def row_iterator_to_df(rows):
    data = [list(row) for row in rows]
    columns = [field.name for field in rows.schema]
    df = pd.DataFrame(data=data, columns=columns)

    return df

def query_english_tag(english_tag):
    query_english_tag_data = f"""
        SELECT {COLUMN_NAME_DATE}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_TAGS}
        WHERE LOWER({COLUMN_NAME_ENGLISH_TAGS}) = LOWER('{english_tag}');
    """

    rows = query(query_english_tag_data)

    data = [list(row)[0] for row in rows]

    return data

def query_planet_names():
    query_planet_names_data = f"""
        SELECT {COLUMN_NAME_NAME}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_PLANET}
        ORDER BY {COLUMN_NAME_PLANET_ID};
    """

    rows = query(query_planet_names_data)

    data = [list(row)[0].lower() for row in rows]

    return data

def query_constellation_names():
    query_constellation_names_data = f"""
        SELECT {COLUMN_NAME_CONSTELLATION_NAME}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_CONSTELLATION}
        ORDER BY {COLUMN_NAME_START_DATE};
    """

    rows = query(query_constellation_names_data)

    data = [list(row)[0].lower() for row in rows]

    return data

def query_comets():
    query_comets_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_COMET};
    """

    rows = query(query_comets_data)
    df = row_iterator_to_df(rows)

    return df

def query_showers():
    query_showers_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_SHOWER};
    """

    rows = query(query_showers_data)
    df = row_iterator_to_df(rows)

    return df

def query_comet_names():
    query_comet_names_data = f"""
        SELECT {COLUMN_NAME_COMET_ID}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_COMET}
        UNION ALL
        SELECT {COLUMN_NAME_NAME}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_COMET};
    """

    rows = query(query_comet_names_data)

    data = [list(row)[0].lower() for row in rows]

    return data

def query_shower_names():
    query_shower_names_data = f"""
        SELECT {COLUMN_NAME_SHOWER}
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_SHOWER};
    """

    rows = query(query_shower_names_data)

    data = [list(row)[0].lower() for row in rows]

    return data

def query_planet(planet_name):
    query_planet_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_PLANET}
        WHERE LOWER({COLUMN_NAME_NAME}) = LOWER('{planet_name}');
    """

    rows = query(query_planet_data)
    df = row_iterator_to_df(rows)

    return df

def query_constellation(constellation_name):
    query_constellation_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_CONSTELLATION}
        WHERE LOWER({COLUMN_NAME_CONSTELLATION_NAME}) = LOWER('{constellation_name}');
    """

    rows = query(query_constellation_data)
    df = row_iterator_to_df(rows)

    return df

def query_comet(comet_name):
    query_comet_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_COMET}
        WHERE LOWER({COLUMN_NAME_COMET_ID}) = LOWER('{comet_name}')
            OR LOWER({COLUMN_NAME_NAME}) = LOWER('{comet_name}');
    """

    rows = query(query_comet_data)
    df = row_iterator_to_df(rows)

    return df

def query_shower(shower_name):
    query_shower_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_SHOWER}
        WHERE LOWER({COLUMN_NAME_SHOWER}) = LOWER('{shower_name}');
    """

    rows = query(query_shower_data)
    df = row_iterator_to_df(rows)

    return df

def query_sun():
    query_sun_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_SUN};
    """

    rows = query(query_sun_data)
    df = row_iterator_to_df(rows)

    return df

def query_apod(date_str):
    query_apod_data = f"""
        SELECT *
        FROM {BQ_PROJECT}.{BQ_DB}.{BQ_TABLE_APOD}
        WHERE {COLUMN_NAME_DATE} = '{date_str}';
    """

    rows = query(query_apod_data)
    df = row_iterator_to_df(rows)

    return df
