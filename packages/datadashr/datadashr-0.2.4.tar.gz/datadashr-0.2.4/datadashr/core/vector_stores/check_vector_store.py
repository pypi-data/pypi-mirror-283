import os


class VectorStoreChecker:
    @staticmethod
    def check_pinecone(api_key):
        if not api_key:
            api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            raise ValueError(
                "API key is required for Pinecone vector store. Set it as an environment variable 'PINECONE_API_KEY'.")
        return api_key

    @staticmethod
    def check_faiss():
        try:
            import faiss
        except ImportError:
            raise ImportError("Faiss library is not installed. Please install it to use Faiss vector store.")

    @staticmethod
    def check_elasticsearch():
        try:
            from elasticsearch import Elasticsearch
        except ImportError:
            raise ImportError(
                "Elasticsearch library is not installed. Please install it to use Elasticsearch vector store.")

    @staticmethod
    def check_qdrant():
        try:
            from qdrant_client import QdrantClient
        except ImportError:
            raise ImportError("Qdrant library is not installed. Please install it to use Qdrant vector store.")

    @staticmethod
    def check_chromadb():
        try:
            from chromadb import Client
        except ImportError:
            raise ImportError("ChromaDB library is not installed. Please install it to use ChromaDB vector store.")
