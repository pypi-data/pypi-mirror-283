from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from datadashr.core.embeddings.check_embeddings import EmbeddingChecker
from typing import Any


class OllamaEmbedding(BaseEmbedding):
    """
    OllamaEmbedding is a concrete implementation of the BaseEmbedding class for the Ollama model.
    It provides methods to check requirements, retrieve embeddings, and embed queries and documents.

    Methods:
        default_model_name(self) -> str:
            Returns the default model name for Ollama.

        check_requirements(self) -> None:
            Checks and ensures that all requirements for using the Ollama model are met.

        get_embedding(self) -> OllamaEmbeddings:
            Retrieves an instance of the OllamaEmbeddings model.

        embed_query(self, query: str) -> Any:
            Embeds a single query using the Ollama model.

        embed_documents(self, document: Any) -> Any:
            Embeds multiple documents using the Ollama model.
    """

    @property
    def default_model_name(self) -> str:
        """
        Return the default model name for Ollama.

        Returns:
            str: The default model name.
        """
        return "nomic-embed-text:latest"

    def check_requirements(self) -> None:
        """
        Checks and ensures that all requirements for using the Ollama model are met.

        Raises:
            ValueError: If the model requirements are not satisfied.
        """
        EmbeddingChecker.check_ollama(self.model_name)

    def get_embedding(self) -> Any:
        """
        Retrieve an instance of the OllamaEmbeddings model.

        Returns:
            OllamaEmbeddings: An instance of the OllamaEmbeddings model.
        """
        self.check_requirements()
        from langchain_community.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(model=self.model_name)

    def embed_query(self, query: str) -> Any:
        """
        Embed a single query using the Ollama model.

        Args:
            query (str): The query to embed.

        Returns:
            Any: The embedding of the query.
        """
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document: Any) -> Any:
        """
        Embed multiple documents using the Ollama model.

        Args:
            document (Any): The documents to embed.

        Returns:
            Any: The embeddings of the documents.
        """
        return self.get_embedding().embed_documents(document)
