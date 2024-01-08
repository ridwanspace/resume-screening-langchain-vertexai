import os
import json
import vertexai
from langchain.embeddings import VertexAIEmbeddings
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the path to the JSON file from the environment variable
json_config_path = os.getenv('SERVICE_ACCOUNT')

# Load the JSON file
with open(json_config_path, 'r') as json_file:
    config = json.load(json_file)

# Set up Vertex AI credentials
credentials = service_account.Credentials.from_service_account_file(json_config_path)
vertexai.init(project=os.getenv("PROJECT_ID"),
              credentials=credentials)


def create_embeddings_load_data():
    """
    Create and load embeddings for data.

    Returns:
        embeddings: An instance of the embeddings class.
    """
    # Create an instance of the VertexAIEmbeddings class.
    embeddings = VertexAIEmbeddings()

    # Return the embeddings instance.
    return embeddings


