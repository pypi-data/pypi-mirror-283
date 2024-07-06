import os
from langchain_openai import OpenAI, AzureChatOpenAI

def azure_openai():
    version = os.getenv('OPENAI_API_VERSION')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    if not version:
        raise ValueError("Environment variable 'OPENAI_API_VERSION' is not set.")
    if not endpoint:
        raise ValueError("Environment variable 'AZURE_OPENAI_ENDPOINT' is not set.")
    if not api_key:
        raise ValueError("Environment variable 'AZURE_OPENAI_API_KEY' is not set.")
    client = AzureChatOpenAI(api_key=api_key,
                         api_version=version,
                         azure_endpoint=endpoint,
                         deployment_name=deployment_name
                         )
    return client

def openai():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Environment variable 'OPENAI_API_KEY' is not set.")
    client = OpenAI(openai_api_key=api_key)
    return client