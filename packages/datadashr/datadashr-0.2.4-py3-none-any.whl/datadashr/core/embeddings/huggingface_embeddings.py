from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from typing import Any


class HuggingfaceEmbedding(BaseEmbedding):
    """
    HuggingfaceEmbedding is a concrete implementation of the BaseEmbedding class for the HuggingFace model.
    It provides methods to check requirements, retrieve embeddings, and embed queries and documents.

    Methods:
        default_model_name(self) -> str:
            Returns the default model name for HuggingFace.

        check_requirements(self) -> None:
            Checks and ensures that all requirements for using the HuggingFace model are met.

        get_embedding(self) -> HuggingFaceEmbeddings:
            Retrieves an instance of the HuggingFaceEmbeddings model.

        embed_query(self, query: str) -> Any:
            Embeds a single query using the HuggingFace model.

        embed_documents(self, document: Any) -> Any:
            Embeds multiple documents using the HuggingFace model.
    """

    @property
    def default_model_name(self) -> str:
        """
        Return the default model name for HuggingFace.

        Returns:
            str: The default model name.
        """
        return "mixedbread-ai/mxbai-embed-large-v1"

    def check_requirements(self) -> None:
        """
        Checks and ensures that all requirements for using the HuggingFace model are met.
        This method can be extended to include specific checks.
        """
        pass

    def get_embedding(self) -> Any:
        """
        Retrieve an instance of the HuggingFaceEmbeddings model.

        Returns:
            HuggingFaceEmbeddings: An instance of the HuggingFaceEmbeddings model.
        """
        self.check_requirements()
        from langchain_huggingface.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=self.model_name)

    def embed_query(self, query: str) -> Any:
        """
        Embed a single query using the HuggingFace model.

        Args:
            query (str): The query to embed.

        Returns:
            Any: The embedding of the query.
        """
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document: Any) -> Any:
        """
        Embed multiple documents using the HuggingFace model.

        Args:
            document (Any): The documents to embed.

        Returns:
            Any: The embeddings of the documents.
        """
        return self.get_embedding().embed_documents(document)
