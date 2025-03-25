import pandas as pd
import boto3
import json
from time import sleep

# Function to generate embeddings using AWS Bedrock
def generate_embedding_with_bedrock(text_data, model_id, region_name="us-west-2"):
    # Initialize the Bedrock client
    bedrock_client = boto3.client("bedrock", region_name=region_name)
    
    # Create the input payload for embedding generation
    payload = {
        "modelId": model_id,
        "body": text_data,
    }
    
    try:
        # Make the request to Bedrock to generate embeddings
        response = bedrock_client.invoke_model(**payload)
        
        # Extract the embeddings from the response
        embeddings = response['body'].read().decode('utf-8')
        embeddings = json.loads(embeddings)  # Convert JSON string to Python object
        
        # Assuming the embedding is in a key like 'embedding' (check response format)
        return embeddings.get('embedding', None)
    
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Function to process the XLSX file and generate embeddings
def process_xlsx_and_generate_embeddings(xlsx_path, model_id, aws_region="us-west-2"):
    # Read the XLSX file using pandas
    df = pd.read_excel(xlsx_path)

    embeddings_data = []

    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        # Concatenate all column values into a single text string
        # Convert each value to string and join them with a space (or other delimiter)
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

# Save embeddings and metadata to a JSON file
def save_embeddings_to_file(embeddings_data, output_file="embeddings_output.json"):
    with open(output_file, 'w') as f:
        json.dump(embeddings_data, f, indent=4)
    print(f"Embeddings and metadata saved to {output_file}")

# Example usage
if __name__ == "__main__":
    xlsx_path = 'your_file.xlsx'  # Path to your XLSX file
    model_id = 'your-bedrock-model-id'  # Replace with your Bedrock model ID
    
    # Process the XLSX file and generate embeddings
    embeddings_data = process_xlsx_and_generate_embeddings(xlsx_path, model_id)

    # Optionally, save the results to a file
    save_embeddings_to_file(embeddings_data)
