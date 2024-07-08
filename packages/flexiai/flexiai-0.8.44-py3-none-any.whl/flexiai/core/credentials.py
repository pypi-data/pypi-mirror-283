# core/credentials.py
import os
from openai import OpenAI, AzureOpenAI
from flexiai.config.config import config
from abc import ABC, abstractmethod

class CredentialStrategy(ABC):
    """
    Abstract base class for credential strategies. This class defines the interface
    for different credential strategies to get their respective API clients.
    """
    
    @abstractmethod
    def get_client(self):
        """
        Abstract method to get the API client.
        
        This method should be implemented by all subclasses to return the appropriate
        client for the given credential strategy.
        
        Returns:
            Client: The API client for the specific credential strategy.
        """
        pass

class OpenAICredentialStrategy(CredentialStrategy):
    """
    Credential strategy for OpenAI.
    
    This class implements the CredentialStrategy interface to provide an OpenAI client
    initialized with the necessary API key and headers.
    """
    
    def get_client(self):
        """
        Get the OpenAI client.
        
        This method retrieves the OpenAI API key from environment variables or the configuration,
        sets up the necessary headers, and returns an OpenAI client instance.
        
        Returns:
            OpenAI: The initialized OpenAI client.
        
        Raises:
            ValueError: If the OpenAI API key is not set.
        """
        api_key = os.getenv("OPENAI_API_KEY", config.OPENAI_API_KEY)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "assistants=v2"
        }
        return OpenAI(api_key=api_key, default_headers=headers)

class AzureOpenAICredentialStrategy(CredentialStrategy):
    """
    Credential strategy for Azure OpenAI.
    
    This class implements the CredentialStrategy interface to provide an Azure OpenAI client
    initialized with the necessary API key and endpoint.
    """
    
    def get_client(self):
        """
        Get the Azure OpenAI client.
        
        This method retrieves the Azure OpenAI API key and endpoint from environment variables
        or the configuration and returns an Azure OpenAI client instance.
        
        Returns:
            AzureOpenAI: The initialized Azure OpenAI client.
        
        Raises:
            ValueError: If the Azure OpenAI API key or endpoint is not set.
        """
        api_key = os.getenv("AZURE_OPENAI_API_KEY", config.AZURE_OPENAI_API_KEY)
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", config.AZURE_OPENAI_ENDPOINT)
        if not api_key or not azure_endpoint:
            raise ValueError("Azure OpenAI API key or endpoint is not set.")
        return AzureOpenAI(
            api_key=api_key,
            api_version="2024-05-01-preview",
            azure_endpoint=azure_endpoint
        )
