import importlib.util
from typing import Optional
from datadashr.config import *


class EmbeddingChecker:
    """
    EmbeddingChecker provides static methods to check and validate the configuration for different embedding models.

    Methods:
        check_openai(model_name: str, api_key: Optional[str]) -> str:
            Validates the model name and API key for OpenAI embedding. Returns the API key if valid.

        check_ollama(model_name: str) -> str:
            Validates the model name for Ollama embedding. Ensures the necessary library is installed
            and the model is available.
    """

    @staticmethod
    def check_openai(model_name: str, api_key: Optional[str] = None) -> str:
        """
        Validate the model name and API key for OpenAI embedding.

        Args:
            model_name (str): The name of the OpenAI model to be used.
            api_key (Optional[str]): The API key for OpenAI. If not provided, the method attempts to fetch
            it from environment variables.

        Returns:
            str: The validated API key.

        Raises:
            ValueError: If the model name or API key is not provided.
        """
        if not model_name:
            raise ValueError("Model name is required for OpenAI embedding.")
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "API key is required for OpenAI embedding. Set it as an environment variable 'OPENAI_API_KEY'.")
        return api_key

    @staticmethod
    def check_ollama(model_name: str) -> str:
        """
        Validate the model name for Ollama embedding and ensure the necessary library is installed.

        Args:
            model_name (str): The name of the Ollama model to be used.

        Returns:
            str: The validated model name.

        Raises:
            ValueError: If the model name is not provided or the model is not available.
            ImportError: If the Ollama library is not installed.
        """
        if not model_name:
            raise ValueError("Model name is required for Ollama embedding.")
        if not importlib.util.find_spec("langchain_community"):
            raise ImportError("Ollama library is not installed. Please install it to use Ollama embeddings.")

        import ollama

        try:
            available_models_response = ollama.list()
            available_models = [model['name'] for model in available_models_response['models']]
        except (TypeError, KeyError, AttributeError) as e:
            logger.warning("Unable to retrieve available models from Ollama API.")
            raise ValueError("Unable to retrieve available models from Ollama API.") from e

        if model_name not in available_models:
            # Install default model
            if model_name == "nomic-embed-text:latest":
                logger.info("Model 'nomic-embed-text:latest' is not available. Installing default model.")
                ollama.pull("nomic-embed-text:latest")
            elif 'embed' in model_name:
                if ':' not in model_name:
                    model_name += ":latest"
                ollama.pull(model_name)
            else:
                logger.error(f"Model '{model_name}' is not available. Available models: {available_models}")
                raise ValueError(f"Model '{model_name}' is not available. Available models: {available_models}")
        return model_name
