from datadashr.core.vector_stores.pinecone_store import PineconeStore
from datadashr.core.vector_stores.faiss_store import FaissStore
from datadashr.core.vector_stores.elasticsearch_store import ElasticsearchStore
from datadashr.core.vector_stores.qdrant_store import QdrantStore
from datadashr.core.vector_stores.chromadb_store import ChromaDBStore


class VectorStore:
    """
    VectorStore is a factory class for creating instances of different vector store types.

    Attributes:
        VECTOR_STORE_CLASSES (dict): A dictionary mapping store types to their corresponding classes.

    Methods:
        __new__(cls, store_type, **kwargs):
            Creates a new instance of the specified vector store type.

        available_stores(cls):
            Returns a list of available vector store types.
    """

    VECTOR_STORE_CLASSES = {
        'pinecone': PineconeStore,
        'faiss': FaissStore,
        'elasticsearch': ElasticsearchStore,
        'qdrant': QdrantStore,
        'chromadb': ChromaDBStore
    }

    def __new__(cls, store_type, **kwargs):
        """
        Create a new instance of the specified vector store type.

        Args:
            store_type (str): The type of vector store to create.
            kwargs: Additional keyword arguments to pass to the vector store class.

        Returns:
            An instance of the specified vector store class.

        Raises:
            ValueError: If the specified store type is not supported.
        """
        if store_type not in cls.VECTOR_STORE_CLASSES:
            raise ValueError(f"Unsupported vector store type: {store_type}")
        store_class = cls.VECTOR_STORE_CLASSES[store_type]
        store_instance = store_class(**kwargs)
        store_instance.get_store()  # Initialize the vector store
        return store_instance

    @classmethod
    def available_stores(cls):
        """
        Return a list of available vector store types.

        Returns:
            list: A list of available vector store types.
        """
        return list(cls.VECTOR_STORE_CLASSES.keys())
