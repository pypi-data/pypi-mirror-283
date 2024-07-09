import importlib.util
from datadashr.config import *


class LLMChecker:
    """
    LLMChecker provides static methods to check and validate the configuration for different Large Language Models.

    Methods:
        check_openai(model_name, api_key):
            Validates the model name and API key for OpenAI LLM. Returns the API key if valid.

        check_groq(model_name, api_key):
            Validates the model name and API key for Groq. Returns the API key if valid.

        check_huggingface(model_name, api_key):
            Validates the model name and API key for Huggingface. Returns the API key if valid.

        check_ollama(model_name):
            Validates the model name for Ollama LLM and ensures the necessary library is installed.
    """

    @staticmethod
    def check_openai(model_name, api_key):
        """
        Validate the model name and API key for OpenAI LLM.

        Args:
            model_name (str): The name of the OpenAI model to be used.
            api_key (str): The API key for OpenAI. If not provided,
            the method attempts to fetch it from environment variables.

        Returns:
            str: The validated API key.

        Raises:
            ValueError: If the model name or API key is not provided.
        """
        if not model_name:
            raise ValueError("Model name is required for OpenAI LLM.")
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("API key is required for OpenAI LLM. Set it as an environment variable 'OPENAI_API_KEY'.")
        return api_key

    @staticmethod
    def check_groq(model_name, api_key):
        """
        Validate the model name and API key for Groq.

        Args:
            model_name (str): The name of the Groq model to be used.
            api_key (str): The API key for Groq. If not provided,
            the method attempts to fetch it from environment variables.

        Returns:
            str: The validated API key.

        Raises:
            ValueError: If the model name or API key is not provided.
        """
        if not model_name:
            raise ValueError("Model name is required for Groq LLM.")
        if not api_key:
            api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("API key is required for Groq. Set it as an environment variable 'GROQ_API_KEY'.")
        return api_key

    @staticmethod
    def check_huggingface(model_name, api_key):
        """
        Validate the model name and API key for Huggingface LLM.

        Args:
            model_name (str): The name of the Huggingface model to be used.
            api_key (str): The API key for Huggingface. If not provided,
            the method attempts to fetch it from environment variables.

        Returns:
            str: The validated API key.

        Raises:
            ValueError: If the model name or API key is not provided.
        """
        if not model_name:
            raise ValueError("Model name is required for Huggingface LLM.")
        if not api_key:
            api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            raise ValueError("API key is required for Huggingface. "
                             "Set it as an environment variable 'HUGGINGFACE_API_KEY'.")
        return api_key

    @staticmethod
    def check_ollama(model_name):
        """
        Validate the model name for Ollama LLM and ensure the necessary library is installed.

        Args:
            model_name (str): The name of the Ollama model to be used.

        Returns:
            str: The validated model name.

        Raises:
            ValueError: If the model name is not provided.
            ImportError: If the Ollama library is not installed.
        """
        if not model_name:
            raise ValueError("Model name is required for Ollama.")
        if not importlib.util.find_spec("langchain_community"):
            raise ImportError("Ollama library is not installed. Please install it to use Ollama embeddings.")

        import ollama

        try:
            available_models_response = ollama.list()
            available_models = [model['name'] for model in available_models_response['models']]
            logger.info(f"Available Ollama models: {available_models}")
        except (TypeError, KeyError, AttributeError) as e:
            logger.warning("Unable to retrieve available models from Ollama API.")
            raise ValueError("Unable to retrieve available models from Ollama API.") from e

        """if model_name not in available_models:
            # install default model
            if model_name == "codestral:latest":
                logger.info("Model 'codestral:latest' is not available. Installing default model.")
                ollama.pull("codestral:latest")
            else:
                logger.error(f"Model '{model_name}' is not available. Available models: {available_models}")
                raise ValueError(f"Model '{model_name}' is not available. Available models: {available_models}")"""
        return model_name
