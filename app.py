import os
from google.cloud import storage
import pandas as pd
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
from google.cloud import bigquery
from consts.const import data_base_name
client = bigquery.Client()


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

def Exec_Query(query):
    results = client.query(query)
    df = results.to_dataframe()
    result_dict = df.to_dict(orient='records')
    return result_dict

@app.route("/")
def hello_world():

    # Construct SQL query
    sql = f"SELECT * FROM `{data_base_name}.{table_name}` ORDER BY id LIMIT 1"

    # Execute query
    original_result = Exec_Query(sql)

    # Repeat the row ten times
    repeated_result = [original_result[0].copy() for _ in range(30)]

    return jsonify(repeated_result)

@app.route("/api/search", methods=["GET"])
def search_data():
    # Get the query parameter from the request URL
    query = request.args.get("query")
    limit = int(request.args.get("limit"))

    if not query:
        return jsonify([])

    # Construct a BigQuery SQL query to search for data
    sql = f"""
    SELECT *
    FROM `{data_base_name}.{table_name}`
    WHERE LOWER(Product_Title) LIKE LOWER('%{query}%')
    OR LOWER(Description) LIKE LOWER('%{query}%')
    LIMIT {limit}
    """
    res = Exec_Query(sql)
    return res


@app.route("/api/products", methods=["GET"])
def get_product():
    id = request.args.get("id")
    if id:
        sql = f"""SELECT
                    *
                    FROM
                    `disney-a2b9f.Wp_Products.products`
                    WHERE
                    id = {id}"""

        res = Exec_Query(sql)
        return res
    else:
        return jsonify([])


@app.route("/api/top_products", methods=["GET"])
def top_product():
    sql = """WITH ranked_products AS (
                    SELECT
                        *,
                        ROW_NUMBER() OVER (PARTITION BY Category_id ORDER BY Category_id) AS rn
                    FROM
                        `disney-a2b9f.Wp_Products.products`
                    )

                    SELECT
                    *
                    FROM
                    ranked_products
                    WHERE
                    rn = 1
                    ORDER BY
                    category_id;"""
    
    res = Exec_Query(sql)
    return res



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
