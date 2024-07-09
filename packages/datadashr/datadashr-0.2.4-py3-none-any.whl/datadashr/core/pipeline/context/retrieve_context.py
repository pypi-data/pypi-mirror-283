from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.vector_stores import VectorStore
from datadashr.core.embeddings import Embedding
from datadashr.config import *


class RetrieveContextStep(DataStep):
    """
    RetrieveContextStep is a pipeline step that retrieves context for a given query by performing a similarity search
    on a vector store and formats the retrieved context. It extends the DataStep class.

    Methods:
        __init__(self, name="RetrieveContext"):
            Initializes the RetrieveContextStep with a default name.

        execute(self, context):
            Retrieves context for a given query by performing a similarity search, formats the context,
            and adds it to the context.
            If an error occurs, it logs the error and sets the retrieved context to an empty string.
    """

    def __init__(self, name="RetrieveContext"):
        """
        Initialize the RetrieveContextStep with a default name.

        Args:
            name (str, optional): The name of the step. Defaults to "RetrieveContext".
        """
        super().__init__(name)

    def execute(self, context):
        """
        Retrieve context for a given query by performing a similarity search, format the context,
        and add it to the context.

        Args:
            context: The context object containing the query, vector store settings, and embedding settings.

        Raises:
            Exception: If an error occurs during the context retrieval, it logs the error and sets
            the retrieved context to an empty string.
        """
        try:
            query = context.request
            vector_settings = context.vector_store
            embedding_settings = context.embedding
            logger.info(f"Query: {query}")
            logger.info(f"Vector Settings: {vector_settings}")
            logger.info(f"Embedding Settings: {embedding_settings}")

            emb = Embedding(
                embedding_type=embedding_settings.get('embedding_type', 'fastembed'),
                model_name=embedding_settings.get('model_name', None),
                api_key=embedding_settings.get('api_key', None)
            )

            vector_instance = VectorStore(
                store_type=vector_settings.get('store_type', 'chromadb'),
                persist_directory=vector_settings.get('persist_directory', None),
                embedding_function=emb.get_embedding()
            )

            logger.info(f"Vector Instance: {vector_instance.__dict__}")

            results = vector_instance.similarity_search(query)
            logger.info(f"Query Results: {results}")

            # Limit the number of documents and the context length
            max_context_length = 2000  # Character limit for the context
            context_text = ""
            for doc in results:
                if len(context_text) + len(doc.page_content) > max_context_length:
                    break
                context_text += doc.page_content + "\n"
                if len(context_text) > max_context_length:
                    break

            context.add_property('retrieved_context', context_text)
            logger.info(f"Retrieved context: {context_text}")
        except Exception as e:
            logger.error(f"Error in RetrieveContextStep: {e}")
            context.add_property('retrieved_context', "")
