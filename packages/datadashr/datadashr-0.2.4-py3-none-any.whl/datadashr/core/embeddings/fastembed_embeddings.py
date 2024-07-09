from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from typing import Any


class FastembedEmbedding(BaseEmbedding):
    """
    FastembedEmbedding is a concrete implementation of the BaseEmbedding class for the FastEmbed model.
    It provides methods to check requirements, retrieve embeddings, and embed queries and documents.

    Methods:
        default_model_name(self) -> str:
            Returns the default model name for FastEmbed.

        check_requirements(self) -> None:
            Checks and ensures that all requirements for using the FastEmbed model are met.

        get_embedding(self) -> FastEmbedEmbeddings:
            Retrieves an instance of the FastEmbedEmbeddings model.

        embed_query(self, query: str) -> Any:
            Embeds a single query using the FastEmbed model.

        embed_documents(self, document: Any) -> Any:
            Embeds multiple documents using the FastEmbed model.
    """

    @property
    def default_model_name(self) -> str:
        """
        Return the default model name for FastEmbed.

        Returns:
            str: The default model name.
        """
        return "BAAI/bge-small-en-v1.5"

    def check_requirements(self) -> None:
        """
        Checks and ensures that all requirements for using the FastEmbed model are met.
        This method can be extended to include specific checks.
        """
        pass

    def get_embedding(self):
        """
        Retrieve an instance of the FastEmbedEmbeddings model.

        Returns:
            FastEmbedEmbeddings: An instance of the FastEmbedEmbeddings model.
        """
        self.check_requirements()
        from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        return FastEmbedEmbeddings()

    def embed_query(self, query: str) -> Any:
        """
        Embed a single query using the FastEmbed model.

        Args:
            query (str): The query to embed.

        Returns:
            Any: The embedding of the query.
        """
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document: Any) -> Any:
        """
        Embed multiple documents using the FastEmbed model.

        Args:
            document (Any): The documents to embed.

        Returns:
            Any: The embeddings of the documents.
        """
        return self.get_embedding().embed_documents(document)
