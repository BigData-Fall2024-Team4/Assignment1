import pymssql
import json
from azure.storage.blob import BlobServiceClient
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def clone_repository():
    """Clones the GAIA GitHub repository if it doesn't exist."""
    GIT_USERNAME = os.getenv("GIT_USERNAME")
    GIT_TOKEN = os.getenv("GIT_TOKEN")
    GIT_REPO_URL = os.getenv("GIT_REPO_URL")
    LOCAL_CLONE_DIR = "./GAIA"

    git_url_with_credentials = GIT_REPO_URL.replace("https://", f"https://{GIT_USERNAME}:{GIT_TOKEN}@")

    if not os.path.exists(LOCAL_CLONE_DIR):
        try:
            print("Cloning the repository...")
            subprocess.run(["git", "clone", git_url_with_credentials, LOCAL_CLONE_DIR], check=True)
            print(f"Cloned repository into {LOCAL_CLONE_DIR}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
    else:
        print(f"Repository already exists at {LOCAL_CLONE_DIR}")

    return LOCAL_CLONE_DIR

def setup_database():
    """Sets up the MSSQL database connection and creates the table if it doesn't exist."""
    conn = pymssql.connect(
        server=os.getenv("MSSQL_SERVER"),
        user=os.getenv("MSSQL_USER"),
        password=os.getenv("MSSQL_PASSWORD"),
        database=os.getenv("MSSQL_DATABASE")
    )
    cursor = conn.cursor()

    # Create table for validation cases if it does not exist
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='validation_cases' AND xtype='U')
        CREATE TABLE validation_cases (
            id INT PRIMARY KEY IDENTITY(1,1),
            task_id VARCHAR(255),
            question TEXT,
            level VARCHAR(50),
            final_answer TEXT,
            file_name VARCHAR(255),
            steps TEXT,
            time_taken VARCHAR(50),
            tools TEXT,
            file_path VARCHAR(500),
            annotator_metadata TEXT
        )
    """)
    conn.commit()

    return conn, cursor

def setup_azure_blob_client():
    """Sets up Azure Blob Storage connection."""
    AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    return container_client

def upload_to_azure(container_client, local_file_path, file_name):
    """Uploads a file to Azure Blob Storage."""
    try:
        blob_client = container_client.get_blob_client(file_name)
        with open(local_file_path, "rb") as data_file:
            blob_client.upload_blob(data_file, overwrite=True)
        print(f"Uploaded {local_file_path} to Azure Blob Storage as {file_name}")
    except Exception as e:
        print(f"Error uploading {local_file_path} to Azure Blob Storage: {e}")

def process_metadata(file_path, cursor, conn, container_client, local_clone_dir):
    """Processes each line in the metadata file, uploads to Azure, and inserts into MSSQL."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return
    
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            task_id = data.get('task_id', 'NULL')
            question = data.get('Question', 'NULL')
            level = data.get('Level', 'NULL')
            final_answer = data.get('Final answer', 'NULL')
            file_name = data.get('file_name', 'NULL')

            annotator_metadata = data.get('Annotator Metadata', {})
            steps = annotator_metadata.get('Steps', 'NULL')
            time_taken = annotator_metadata.get('How long did this take?', 'NULL')
            tools = annotator_metadata.get('Tools', 'NULL')

            # Upload to Azure if file_name is present
            if file_name and file_name != 'NULL':
                local_file_path = os.path.join(local_clone_dir, '2023', 'validation', file_name)
                if os.path.exists(local_file_path):
                    upload_to_azure(container_client, local_file_path, file_name)
                else:
                    print(f"File {local_file_path} not found in the GAIA dataset.")
            
            # Insert data into MSSQL
            sql = """
            INSERT INTO validation_cases (task_id, question, level, final_answer, file_name, steps, time_taken, tools, file_path, annotator_metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (task_id, question, level, final_answer, file_name, steps, time_taken, tools, local_file_path if file_name else 'NULL', json.dumps(annotator_metadata))
            cursor.execute(sql, values)
            conn.commit()

    print("Data inserted and files uploaded successfully.")

def main():
    local_clone_dir = clone_repository()
    file_path = os.path.join(local_clone_dir, '2023', 'validation', 'metadata.jsonl')
    conn, cursor = setup_database()
    container_client = setup_azure_blob_client()

    process_metadata(file_path, cursor, conn, container_client, local_clone_dir)

if __name__ == "__main__":
    main()
