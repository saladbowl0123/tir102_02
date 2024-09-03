from google.cloud import bigquery

client = bigquery.Client()

def query(query):
    query_job = client.query(query)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row)
    
    return rows
