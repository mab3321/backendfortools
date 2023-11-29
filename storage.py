import firebase_admin
from firebase_admin import credentials, storage

def download_and_print_file(storage_bucket, file_path):
    """
    Downloads a file from Firebase Storage and prints its data.

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

        # Print the file content
        print(f"File content:\n{file_content}")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Example usage
storage_bucket = "disney-a2b9f.appspot.com"
file_path = "encrypted_data_netflix.txt"

download_and_print_file(storage_bucket, file_path)
