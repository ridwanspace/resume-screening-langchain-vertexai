import os
import json
from dotenv import load_dotenv
from langchain.llms import VertexAI
from langchain.chains.summarize import load_summarize_chain


# PaLM 
from langchain.llms import VertexAI
from google.oauth2 import service_account
import vertexai

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



def get_summary(current_doc):
    """
    Get a summary of the given document using a pre-trained model.
    
    Args:
        current_doc (str): The document to be summarized.
        
    Returns:
        str: The summary of the document.
    """
    # Initialize the VertexAI model with the appropriate parameters
    llm = VertexAI(
        model_name="text-bison@001", 
        temperature=0,
        max_output_tokens=256
    )
    
    # Load the summarize chain using the model
    chain = load_summarize_chain(llm, chain_type="stuff") # you may choose map_reduce or refine as well, refer to the langchain docs for more info
    
    # Generate the summary for the current document
    summary = chain.run([current_doc])
    
    return summary
