import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_openai_api_key():
    """
    Retrieve the OpenAI API key from environment variables.
    Returns:
        str: The OpenAI API key
    Raises:
        ValueError: If the API key is not found in environment variables
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or .env file.")
    return api_key

def get_serper_api_key():
    """
    Retrieve the Serper API key from environment variables.
    Returns:
        str: The Serper API key
    Raises:
        ValueError: If the API key is not found in environment variables
    """
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        raise ValueError("Serper API key not found. Please set SERPER_API_KEY in your environment variables or .env file.")
    return api_key
