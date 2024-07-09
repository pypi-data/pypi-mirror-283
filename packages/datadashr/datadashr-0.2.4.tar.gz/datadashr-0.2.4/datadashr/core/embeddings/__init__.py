from datadashr.core.embeddings.openai_embeddings import OpenAIEmbedding
from datadashr.core.embeddings.ollama_embeddings import OllamaEmbedding
from datadashr.core.embeddings.fastembed_embeddings import FastembedEmbedding
from datadashr.core.embeddings.huggingface_embeddings import HuggingfaceEmbedding


class Embedding:
    """
    Embedding is a factory class that provides an interface for creating and managing various types of embedding models.
    It supports OpenAI, Ollama, Fastembed, and Huggingface embeddings.

    Attributes:
        EMBEDDING_CLASSES (dict): A dictionary mapping embedding type names to their corresponding classes.

    Methods:
        __new__(cls, embedding_type, model_name=None, api_key=None):
            Creates a new instance of the specified embedding type.

        available_embeddings(cls):
            Returns a list of available embedding types.
    """

    EMBEDDING_CLASSES = {
        'openai': OpenAIEmbedding,
        'ollama': OllamaEmbedding,
        'fastembed': FastembedEmbedding,
        'huggingface': HuggingfaceEmbedding
    }

    def __new__(cls, embedding_type: str, model_name: str = None, api_key: str = None):
        """
        Create a new instance of the specified embedding type.

        Args:
            embedding_type (str): The type of embedding to create (e.g., 'openai', 'ollama', 'fastembed', 'huggingface').
            model_name (str, optional): The name of the model to use. Defaults to the default model name of the embedding class.
            api_key (str, optional): The API key for accessing the embedding model. Defaults to None.

        Returns:
            BaseEmbedding: An instance of the specified embedding class.

        Raises:
            ValueError: If the specified embedding type is not supported.
        """
        if embedding_type not in cls.EMBEDDING_CLASSES:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")
        embedding_class = cls.EMBEDDING_CLASSES[embedding_type]
        embedding_instance = embedding_class(model_name, api_key)
        embedding_instance.get_embedding()  # Initialize the embedding model
        return embedding_instance

    @classmethod
    def available_embeddings(cls):
        """
        Return a list of available embedding types.

        Returns:
            list: A list of available embedding types.
        """
        return list(cls.EMBEDDING_CLASSES.keys())
