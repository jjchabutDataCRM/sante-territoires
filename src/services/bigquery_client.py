from google.cloud import bigquery

def run_query(query):
    client = bigquery.Client(project="sante-et-territoires")
    query_job = client.query(query)
    return query_job.result().to_dataframe()