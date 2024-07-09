from typing import Any, Optional


class BaseEmbedding:
    """
    BaseEmbedding is an abstract base class for embedding models. It provides a common interface for
    different embedding models, including methods for checking requirements, retrieving embeddings, and
    accessing model information.

    Attributes:
        model_name (str): The name of the embedding model.
        api_key (str): The API key for accessing the embedding model.
        embedding_model (Any): The instance of the embedding model.
    """

    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None) -> None:
        """
        Initialize the BaseEmbedding instance with a model name and an API key.

        Args:
            model_name (Optional[str]): The name of the embedding model. If not provided,
            the default model name is used.
            api_key (Optional[str]): The API key for accessing the embedding model.
        """
        self.model_name = model_name or self.default_model_name
        self.api_key = api_key
        self.embedding_model = None

    @property
    def default_model_name(self) -> str:
        """
        Abstract property that should be implemented by subclasses to return the default model name.

        Returns:
            str: The default model name.

        Raises:
            NotImplementedError: If the subclass does not implement this property.
        """
        raise NotImplementedError("Subclasses should implement this property.")

    def check_requirements(self) -> None:
        """
        Abstract method that should be implemented by subclasses to check the requirements for the embedding model.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_embedding(self) -> Any:
        """
        Abstract method that should be implemented by subclasses to retrieve the embedding for a given text.

        Returns:
            Any: The embedding model instance.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def embed_query(self, query: str) -> Any:
        """
        Abstract method that should be implemented by subclasses to embed a single query.

        Args:
            query (str): The query to embed.

        Returns:
            Any: The embedding of the query.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def embed_documents(self, documents: Any) -> Any:
        """
        Abstract method that should be implemented by subclasses to embed multiple documents.

        Args:
            documents (Any): The documents to embed.

        Returns:
            Any: The embeddings of the documents.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def model_info(self) -> dict:
        """
        Property that returns a dictionary containing model information.

        Returns:
            dict: A dictionary containing the model name and API key.
        """
        return {
            "model_name": self.model_name,
            "api_key": self.api_key
        }
