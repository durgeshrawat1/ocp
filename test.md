from pymongo import MongoClient
import boto3
import json
from time import sleep
import pandas as pd

# Set up AWS DocumentDB connection using pymongo (MongoDB client)
def connect_to_documentdb(host, port, username, password, db_name):
    # Define the connection URI for DocumentDB
    uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
    client = MongoClient(uri)
    return client[db_name]  # Returns the specific database

# Specify your DocumentDB details
docdb_host = "your-documentdb-cluster-endpoint"
docdb_port = 27017  # Default port for MongoDB/DocumentDB
docdb_username = "your-username"
docdb_password = "your-password"
docdb_db_name = "your-database-name"
docdb_collection_name = "your-collection-name"


---

# Function to save embedding and metadata to DocumentDB
def save_to_documentdb(embedding_data, db):
    collection = db[docdb_collection_name]
    
    # Insert data as documents in the collection
    for data in embedding_data:
        document = {
            "index": data["index"],  # Save the row index
            "embedding": data["embedding"],  # Save the embedding vector
            "metadata": data["metadata"],  # Save all the metadata (row data from XLSX)
        }
        
        # Insert document into the collection
        collection.insert_one(document)
        print(f"Document {data['index'] + 1} inserted into DocumentDB.")

# Function to process the XLSX file and generate embeddings
def process_xlsx_and_generate_embeddings(xlsx_path, model_id, aws_region="us-west-2"):
    # Read the XLSX file using pandas
    df = pd.read_excel(xlsx_path)

    embeddings_data = []

    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        # Concatenate all column values into a single text string
        text_data = " ".join([str(value) for value in row.values])
        
        # Generate the embedding using AWS Bedrock
        embedding = generate_embedding_with_bedrock(text_data, model_id, region_name=aws_region)
        
        if embedding:
            # Store metadata along with the embeddings (entire row is metadata)
            metadata = row.to_dict()  # Convert the entire row to metadata (all columns)
            embeddings_data.append({
                "index": index,
                "metadata": metadata,
                "embedding": embedding
            })
            print(f"Processed row {index + 1}: Embedding generated.")
        else:
            print(f"Error processing row {index + 1}: No embedding generated.")

        # To avoid hitting rate limits (if applicable)
        sleep(0.5)  # Adjust based on your needs or API rate limits
    
    return embeddings_data

# Example usage
if __name__ == "__main__":
    xlsx_path = 'your_file.xlsx'  # Path to your XLSX file
    model_id = 'your-bedrock-model-id'  # Replace with your Bedrock model ID
    
    # Process the XLSX file and generate embeddings
    embeddings_data = process_xlsx_and_generate_embeddings(xlsx_path, model_id)

    # Connect to DocumentDB
    db = connect_to_documentdb(docdb_host, docdb_port, docdb_username, docdb_password, docdb_db_name)

    # Save embeddings and metadata to DocumentDB
    save_to_documentdb(embeddings_data, db)


---
{
  "index": 0,
  "embedding": [0.12, 0.34, 0.56, ...],  # Embedding vector (float array)
  "metadata": {
    "ID": 1,
    "Title": "Title A",
    "Description": "Description A",
    "Author": "Author A",
    "Date": "2021-01-01",
    "Category": "Category1",
    "Keywords": "keyword1,2",
    "Additional Info": "More info 1"
  }
}
