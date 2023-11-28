from flask import Flask, jsonify,request
from cryptography.fernet import Fernet
from flask_cors import CORS
import json
from flask import send_file

app = Flask(__name__)
CORS(app)
@app.route('/return-files')
def return_files_tut():
    try:
        # Get the 'id' parameter from the query string
        file_name = request.args.get('name')

        # Use the file_id in your logic
        # For example, you can construct the file path based on the id
        file_path = f'C:\\Users\\MAB\\Downloads\\encrypted_data_{file_name}.txt'

        # Send the file as a response
        return send_file(file_path, attachment_filename='data.txt')
    except Exception as e:
        return str(e)
if __name__ == '__main__':
    app.run(debug=True)
