import os
import pandas as pd
import random
from flask import Flask, jsonify, request,send_file
from flask_cors import CORS
import csv
from consts.const import data_base_name
from flask import Flask, send_file, request
import firebase_admin
from firebase_admin import credentials, storage
import io
def download_file_from_storage(storage_bucket, file_path):
    """
    Downloads a file from Firebase Storage and returns its content.

    Parameters:
        - storage_bucket: The name of your Firebase Storage bucket.
        - file_path: The path to the file in the bucket.
    """

    # Initialize Firebase with the credentials file
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})

    # Create a storage client
    storage_client = storage.bucket()

    # Get a reference to the file
    blob = storage_client.blob(file_path)

    try:
        # Download the file
        file_content = blob.download_as_text()

        # Return the file content
        return file_content
    except Exception as e:
        return f"Error downloading file: {e}"



app = Flask(__name__)
CORS(app)
table_name = "products"


# def read_file(bucket_name="disney-a2b9f.appspot.com", blob_name="output.csv"):
#     """Read a CSV blob from GCS using file-like IO"""

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(blob_name)

#     # Open the blob for reading
#     file = blob.open("r", encoding="utf-8")

#     return file


# def read_data_from_csv(csv_file):
#     data = []

#     # Use the CSV reader to read data from the file
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         data.append(row)

#     return data

# def Exec_Query(query):
#     results = client.query(query)
#     df = results.to_dataframe()
#     result_dict = df.to_dict(orient='records')
#     return jsonify(result_dict)
# # Specify the path to your CSV file and encoding
# # csv_file_path = read_file()  # Replace with the path to your CSV file
# # csv_encoding = 'utf-8'  # Replace with the appropriate encoding if needed

# # # Read data from the CSV file
# # data = read_data_from_csv(csv_file_path)


# @app.route("/")
# def hello_world():

#     sql = f"""
#         SELECT * FROM `{data_base_name}.{table_name}` order by id LIMIT 10
#     """
#     res = Exec_Query(sql)
#     return res

# def Exec_Query(query):
#     results = client.query(query)
#     df = results.to_dataframe()
#     result_dict = df.to_dict(orient='records')
#     return result_dict

# @app.route("/")
# def hello_world():

#     # Construct SQL query
#     sql = f"SELECT * FROM `{data_base_name}.{table_name}` ORDER BY id LIMIT 1"

#     # Execute query
#     original_result = Exec_Query(sql)

#     return jsonify(original_result)

# @app.route("/api/search", methods=["GET"])
# def search_data():
#     # Get the query parameter from the request URL
#     query = request.args.get("query")
#     limit = int(request.args.get("limit"))

#     if not query:
#         return jsonify([])

#     # Construct a BigQuery SQL query to search for data
#     sql = f"""
#     SELECT *
#     FROM `{data_base_name}.{table_name}`
#     WHERE LOWER(Product_Title) LIKE LOWER('%{query}%')
#     OR LOWER(Description) LIKE LOWER('%{query}%')
#     LIMIT {limit}
#     """
#     res = Exec_Query(sql)
#     return res


# @app.route("/api/products", methods=["GET"])
# def get_product():
#     id = request.args.get("id")
#     if id:
#         sql = f"""SELECT
#                     *
#                     FROM
#                     `disney-a2b9f.Wp_Products.products`
#                     WHERE
#                     id = {id}"""

#         res = Exec_Query(sql)
#         return res
#     else:
#         return jsonify([])


# @app.route("/api/top_products", methods=["GET"])
# def top_product():
#     sql = """WITH ranked_products AS (
#                     SELECT
#                         *,
#                         ROW_NUMBER() OVER (PARTITION BY Category_id ORDER BY Category_id) AS rn
#                     FROM
#                         `disney-a2b9f.Wp_Products.products`
#                     )

#                     SELECT
#                     *
#                     FROM
#                     ranked_products
#                     WHERE
#                     rn = 1
#                     ORDER BY
#                     category_id;"""
    
#     res = Exec_Query(sql)
#     return res


@app.route('/return-files')
def return_files_tut():
    try:
        # Get the 'name' parameter from the query string
        file_name = request.args.get('name')

        # Use the file_name in your logic
        # For example, you can construct the file path based on the name
        file_path = f'encrypted_data_netflix.txt'
        
        # Download the file content
        file_content = download_file_from_storage("disney-a2b9f.appspot.com", file_path)

        # Send the file content as a response
        return send_file(
            io.BytesIO(file_content.encode()),
            attachment_filename=f"{file_name}.txt",
            as_attachment=True
        )
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
