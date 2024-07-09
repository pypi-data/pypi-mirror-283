import elasticsearch
from langchain_community.vectorstores import ElasticsearchStore as LangchainElasticsearchStore
from langchain_core.documents import Document
from langchain_community.vectorstores.utils import filter_complex_metadata
from datadashr.core.vector_stores.base_vector_store import BaseVectorStore
from datadashr.core.vector_stores.check_vector_store import VectorStoreChecker
from datadashr.config import *
from datetime import datetime


class ElasticsearchStore(BaseVectorStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.docs = []
        self.get_store()

    def check_requirements(self):
        VectorStoreChecker.check_elasticsearch()

    def get_store(self):
        self.check_requirements()
        self.hosts = self.kwargs.get('hosts', ["http://localhost:9200"])
        self.es_user = self.kwargs.get('es_user', 'elastic')
        self.es_password = self.kwargs.get('es_password', 'changeme')
        self.index_name = self.kwargs.get('index_name', 'test_index')

        self.es_client = elasticsearch.Elasticsearch(
            hosts=self.hosts,
            http_auth=(self.es_user, self.es_password),
            max_retries=10,
        )

        self.embedding_function = self.kwargs['embedding_function']
        self.store = None

    @property
    def store_info(self):
        return {
            "hosts": self.hosts,
            "index_name": self.index_name
        }

    def similarity_search(self, query):
        return [] if self.store is None else self.store.similarity_search(query)

    def add_texts(self, texts, metadata=None):
        if metadata is None:
            metadata = [{} for _ in range(len(texts))]
        documents = [Document(page_content=text, metadata=meta) for text, meta in zip(texts, metadata)]
        self.docs.extend(documents)
        if self.store is None:
            self.store = LangchainElasticsearchStore.from_texts(
                [doc.page_content for doc in self.docs],
                self.embedding_function,
                metadatas=[doc.metadata for doc in self.docs],
                es_connection=self.es_client,
                index_name=self.index_name
            )
        else:
            self.store.add_texts([doc.page_content for doc in documents], [doc.metadata for doc in documents])

    def add_dataframe(self, df, source=None, additional_metadata=None, overwrite_rule=None, days_threshold=None):
        self._process_pandas_dataframe(df, source)
        self.store = LangchainElasticsearchStore.from_documents(
            self.docs,
            self.embedding_function,
            es_connection=self.es_client,
            index_name=self.index_name
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
        self.store.client.delete(index=self.index_name, id=document_id)

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
            self.store = LangchainElasticsearchStore.from_documents(
                self.docs,
                self.embedding_function,
                es_connection=self.es_client,
                index_name=self.index_name
            )

    def manage_metadata(self, documents, source, file_type, overwrite_rule="always", days_threshold=2):
        return super().manage_metadata(documents, source, file_type, overwrite_rule, days_threshold)

    def check_and_update(self, documents, source, update_interval_days=2):
        return super().check_and_update(documents, source, update_interval_days)

    def get_all_documents(self):
        return self.docs

    def ntotal(self):
        return self.store.client.count(index=self.index_name)['count'] if self.store else 0
