from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from datadashr.core.vector_stores.base_vector_store import BaseVectorStore
from datadashr.core.vector_stores.check_vector_store import VectorStoreChecker
from langchain_community.vectorstores.utils import filter_complex_metadata
from datadashr.config import *
from datetime import datetime
import chromadb.errors
import uuid


class ChromaDBStore(BaseVectorStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.docs = []
        self.get_store()

    def check_requirements(self):
        VectorStoreChecker.check_chromadb()

    def get_store(self):
        self.check_requirements()
        self.embedding_function = self.kwargs['embedding_function']
        self.persist_directory = self.kwargs.get('persist_directory', None)
        self.collection_name = self.kwargs.get('collection_name', 'datadashr')
        self.store = Chroma(collection_name=self.collection_name, persist_directory=self.persist_directory,
                            embedding_function=self.embedding_function)
        self.docs = self.get_all_documents()

    @property
    def store_info(self):
        return {
            "persist_directory": self.persist_directory,
            "document_path": self.kwargs.get('document_path', './document.txt')
        }

    def similarity_search(self, query):
        return [] if self.store is None else self.store.similarity_search(query)

    def add_texts(self, texts, metadata=None):
        if metadata is None:
            metadata = [{} for _ in range(len(texts))]
        documents = [Document(page_content=text, metadata={**meta, 'id': str(uuid.uuid4())}) for text, meta in
                     zip(texts, metadata)]
        self.docs.extend(documents)
        try:
            if self.store is None:
                self.store = Chroma.from_texts([doc.page_content for doc in self.docs], self.embedding_function,
                                               metadatas=[doc.metadata for doc in self.docs],
                                               persist_directory=self.persist_directory,
                                               collection_name=self.collection_name)
            else:
                self.store.add_texts([doc.page_content for doc in documents], [doc.metadata for doc in documents])
        except chromadb.errors.InvalidDimensionException as e:
            logger.warning(f"Invalid dimension exception encountered: {e}. Recreating the collection.")
            self.reset_and_recreate_collection()

    def add_dataframe(self, df, source=None, additional_metadata=None, overwrite_rule=None, days_threshold=None):
        self._process_pandas_dataframe(df, source)
        try:
            self.store = Chroma.from_documents(self.docs, self.embedding_function,
                                               persist_directory=self.persist_directory)
        except chromadb.errors.InvalidDimensionException as e:
            logger.warning(f"Invalid dimension exception encountered: {e}. Recreating the collection.")
            self.reset_and_recreate_collection()

    def _process_pandas_dataframe(self, df, source):
        for _, row in df.iterrows():
            metadata = {
                'source': source or 'pandas_dataframe',
                'dataframe_type': 'pandas',
                'date': datetime.utcnow().isoformat(),
                'id': str(uuid.uuid4())
            }
            metadata.update({f'col_{col}': row[col] for col in df.columns})
            document = Document(page_content=str(row.to_dict()), metadata=metadata)
            filtered_documents = filter_complex_metadata([document])  # Filtra i metadati complessi
            self.docs.extend(filtered_documents)

    def update_document(self, document_id, document):
        self.store.update_document(document_id, document)

    def delete_document(self, document_id):
        self.store._collection.delete(ids=[document_id])
        self.docs = [doc for doc in self.docs if doc.metadata['id'] != document_id]

    def reset_and_recreate_collection(self):
        logger.info("Resetting the collection.")
        if self.store:
            self.store.delete_collection()  # Delete the entire collection

        self.store = Chroma(collection_name=self.collection_name, persist_directory=self.persist_directory,
                            embedding_function=self.embedding_function)
        self.store.add_texts([doc.page_content for doc in self.docs], [doc.metadata for doc in self.docs])

    def delete_documents_by_metadata(self, source=None, start_date=None, end_date=None):
        to_keep = []
        to_delete = []
        for doc in self.docs:
            if source and doc.metadata.get("source") != source:
                to_keep.append(doc)
                continue
            doc_date = datetime.fromisoformat(doc.metadata.get("date"))
            if start_date and doc_date < start_date:
                to_keep.append(doc)
                continue
            if end_date and doc_date > end_date:
                to_keep.append(doc)
                continue
            to_delete.append(doc.metadata['id'])

        self.docs = to_keep
        if to_delete:
            self.store._collection.delete(ids=to_delete)

        if not self.docs:
            self.store = None  # Inizializza con None se non ci sono documenti
        else:
            if self.persist_directory:
                self.store = Chroma.from_documents(self.docs, self.embedding_function,
                                                   persist_directory=self.persist_directory,
                                                   collection_name=self.collection_name)
            else:
                self.store = Chroma.from_documents(self.docs, self.embedding_function)

    def manage_metadata(self, documents, source, file_type, overwrite_rule="always", days_threshold=2):
        return super().manage_metadata(documents, source, file_type, overwrite_rule, days_threshold)

    def check_and_update(self, documents, source, update_interval_days=2):
        return super().check_and_update(documents, source, update_interval_days)

    def get_all_documents(self):
        return self.docs

    def ntotal(self):
        return self.store.index.ntotal if self.store else 0
