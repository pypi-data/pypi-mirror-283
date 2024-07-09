from langchain_core.documents import Document
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_qdrant import Qdrant as LangchainQdrant
from datadashr.core.vector_stores.base_vector_store import BaseVectorStore
from datadashr.core.vector_stores.check_vector_store import VectorStoreChecker
from datadashr.config import *
from datetime import datetime


class QdrantStore(BaseVectorStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.docs = []
        self.get_store()

    def check_requirements(self):
        VectorStoreChecker.check_qdrant()

    def get_store(self):
        self.check_requirements()

        location = self.kwargs.get('location', None)
        path = self.kwargs.get('path', None)
        url = self.kwargs.get('url', None)
        api_key = self.kwargs.get('api_key', None)
        prefer_grpc = self.kwargs.get('prefer_grpc', False)
        collection_name = self.kwargs.get('collection_name', 'my_documents')
        force_recreate = self.kwargs.get('force_recreate', False)

        self.embedding_function = self.kwargs['embedding_function']

        if location:
            self.store = LangchainQdrant.from_documents(
                self.docs, self.embedding_function, location=location, collection_name=collection_name
            )
        elif path:
            self.store = LangchainQdrant.from_documents(
                self.docs, self.embedding_function, path=path, collection_name=collection_name
            )
        elif url:
            self.store = LangchainQdrant.from_documents(
                self.docs, self.embedding_function, url=url, api_key=api_key, prefer_grpc=prefer_grpc,
                collection_name=collection_name, force_recreate=force_recreate
            )
        else:
            raise ValueError("Either 'location', 'path', or 'url' must be provided for Qdrant configuration.")

    @property
    def store_info(self):
        return {
            "location": self.kwargs.get('location'),
            "path": self.kwargs.get('path'),
            "url": self.kwargs.get('url'),
            "collection_name": self.kwargs.get('collection_name', 'my_documents')
        }

    def similarity_search(self, query):
        return [] if self.store is None else self.store.similarity_search(query)

    def similarity_search_with_score(self, query):
        return [] if self.store is None else self.store.similarity_search_with_score(query)

    def add_texts(self, texts, metadata=None):
        if metadata is None:
            metadata = [{} for _ in range(len(texts))]
        documents = [Document(page_content=text, metadata=meta) for text, meta in zip(texts, metadata)]
        self.docs.extend(documents)
        if self.store is None:
            self.store = LangchainQdrant.from_texts(
                [doc.page_content for doc in self.docs],
                self.embedding_function,
                metadatas=[doc.metadata for doc in self.docs],
                url=self.kwargs.get('url'),
                api_key=self.kwargs.get('api_key'),
                prefer_grpc=self.kwargs.get('prefer_grpc'),
                collection_name=self.kwargs.get('collection_name'),
                force_recreate=self.kwargs.get('force_recreate')
            )
        else:
            self.store.add_texts([doc.page_content for doc in documents], [doc.metadata for doc in documents])

    def add_dataframe(self, df, source=None, additional_metadata=None, overwrite_rule=None, days_threshold=None):
        self._process_pandas_dataframe(df, source)
        self.store = LangchainQdrant.from_documents(
            self.docs,
            self.embedding_function,
            url=self.kwargs.get('url'),
            api_key=self.kwargs.get('api_key'),
            prefer_grpc=self.kwargs.get('prefer_grpc'),
            collection_name=self.kwargs.get('collection_name'),
            force_recreate=self.kwargs.get('force_recreate')
        )

    def _process_pandas_dataframe(self, df, source):
        for _, row in df.iterrows():
            metadata = {
                'source': source or 'pandas_dataframe',
                'dataframe_type': 'pandas',
                'date': datetime.utcnow().isoformat()
            }
            metadata.update({f'col_{col}': row[col] for col in df.columns})
            document = Document(page_content=str(row.to_dict()), metadata=metadata)
            filtered_documents = filter_complex_metadata([document])  # Filtra i metadati complessi
            self.docs.extend(filtered_documents)

    def update_document(self, document_id, document):
        self.store.update_document(document_id, document)

    def delete_document(self, document_id):
        self.store._collection.delete(ids=[document_id])

    def reset_collection(self):
        self.docs = []
        self.store = None  # Inizializza con None se non ci sono documenti

    def delete_documents_by_metadata(self, source=None, start_date=None, end_date=None):
        to_keep = []
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

        self.docs = to_keep
        if not self.docs:
            self.store = None  # Inizializza con None se non ci sono documenti
        else:
            self.store = LangchainQdrant.from_documents(
                self.docs,
                self.embedding_function,
                url=self.kwargs.get('url'),
                api_key=self.kwargs.get('api_key'),
                prefer_grpc=self.kwargs.get('prefer_grpc'),
                collection_name=self.kwargs.get('collection_name'),
                force_recreate=self.kwargs.get('force_recreate')
            )

    def manage_metadata(self, documents, source, file_type, overwrite_rule="always", days_threshold=2):
        return super().manage_metadata(documents, source, file_type, overwrite_rule, days_threshold)

    def check_and_update(self, documents, source, update_interval_days=2):
        return super().check_and_update(documents, source, update_interval_days)

    def get_all_documents(self):
        return self.docs

    def ntotal(self):
        return self.store.index.ntotal if self.store else 0
