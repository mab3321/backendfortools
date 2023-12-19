from pandas_gbq import to_gbq
from google.cloud import bigquery
import pandas as pd

# Replace with your Google Cloud project ID
project_id = "propane-surfer-408115"

# Initialize a BigQuery client
client = bigquery.Client(project=project_id)

# Define the BigQuery dataset and table information
dataset_id = "tools"  # Replace with your dataset ID
table_id = "products"  # Replace with your table ID

# Replace with the path to your CSV file
csv_file_path = r"c:\Users\MAB\Downloads\Backend\data.csv"

# Load the CSV data into a Pandas DataFrame
data_frame = pd.read_csv(csv_file_path)

# Define the destination table
destination_table = f"{project_id}.{dataset_id}.{table_id}"

# Load the Pandas DataFrame into BigQuery
job_config = bigquery.LoadJobConfig(
    # Change to WRITE_APPEND or WRITE_EMPTY if needed
    write_disposition="WRITE_APPEND",
    autodetect=True,
    max_bad_records=0    # Set to False if you want to provide a specific schema
)
# print(data_frame['Image-src'])
job = client.load_table_from_dataframe(
    data_frame, destination_table, job_config=job_config)
job.result()  # Wait for the job to complete

print(f"Data loaded into BigQuery table {destination_table}")
