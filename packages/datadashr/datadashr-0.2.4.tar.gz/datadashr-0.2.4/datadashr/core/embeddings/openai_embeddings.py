from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from datadashr.core.embeddings.check_embeddings import EmbeddingChecker
from typing import Any


class OpenAIEmbedding(BaseEmbedding):
    """
    OpenAIEmbedding is a concrete implementation of the BaseEmbedding class for the OpenAI model.
    It provides methods to check requirements, retrieve embeddings, and embed queries and documents.

    Methods:
        default_model_name(self) -> str:
            Returns the default model name for OpenAI.

        check_requirements(self) -> None:
            Checks and ensures that all requirements for using the OpenAI model are met.

        get_embedding(self) -> OpenAIEmbeddings:
            Retrieves an instance of the OpenAIEmbeddings model.

        embed_query(self, query: str) -> Any:
            Embeds a single query using the OpenAI model.

        embed_documents(self, document: Any) -> Any:
            Embeds multiple documents using the OpenAI model.
    """

    @property
    def default_model_name(self) -> str:
        """
        Return the default model name for OpenAI.

        Returns:
            str: The default model name.
        """
        return "text-embedding-ada-002"

    def check_requirements(self) -> None:
        """
        Checks and ensures that all requirements for using the OpenAI model are met.

        Raises:
            ValueError: If the model requirements are not satisfied.
        """
        self.api_key = EmbeddingChecker.check_openai(self.model_name, self.api_key)

    def get_embedding(self) -> Any:
        """
        Retrieve an instance of the OpenAIEmbeddings model.

        Returns:
            OpenAIEmbeddings: An instance of the OpenAIEmbeddings model.
        """
        self.check_requirements()
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=self.model_name, api_key=self.api_key)

    def embed_query(self, query: str) -> Any:
        """
        Embed a single query using the OpenAI model.

        Args:
            query (str): The query to embed.

        Returns:
            Any: The embedding of the query.
        """
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document: Any) -> Any:
        """
        Embed multiple documents using the OpenAI model.

        Args:
            document (Any): The documents to embed.

        Returns:
            Any: The embeddings of the documents.
        """
        return self.get_embedding().embed_documents(document)
