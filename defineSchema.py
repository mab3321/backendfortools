from pandas_gbq import to_gbq
from google.cloud import bigquery
import pandas as pd

# Replace "data.csv" with the path to your CSV file
csv_file = r"C:\Users\MAB\Downloads\Backend\data.csv";

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)
# Define the schema for your table
# Define the schema for your table as a list of dictionaries
# Define your schema
schema = [
    bigquery.SchemaField('id', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('name', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('description', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('hidden_text', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('image_url', 'STRING', mode='NULLABLE'),
]

# Define the BigQuery client
client = bigquery.Client(project='propane-surfer-408115')

# Define the dataset and table IDs
dataset_id = 'tools'
table_id = 'products'

# Create the table with the specified schema
table_ref = client.dataset(dataset_id).table(table_id)
table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table)  # This line actually creates the table

print(f"Table {table_id} created with the specified schema.")

# Now you can load your data into this table
# to_gbq(df, f"{project_id}.{dataset_id}.{table_id}", if_exists='replace')
# print("DONE")
