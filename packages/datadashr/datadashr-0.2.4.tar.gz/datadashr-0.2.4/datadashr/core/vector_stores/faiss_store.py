from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import filter_complex_metadata
from datadashr.core.vector_stores.base_vector_store import BaseVectorStore
from datadashr.core.vector_stores.check_vector_store import VectorStoreChecker
from datadashr.config import *
from datetime import datetime
import os


class FaissStore(BaseVectorStore):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.docs = []
        self.allow_dangerous_deserialization = kwargs.get('allow_dangerous_deserialization', True)
        self.get_store()

    def check_requirements(self):
        VectorStoreChecker.check_faiss()

    def get_store(self):
        self.check_requirements()
        self.embedding_function = self.kwargs['embedding_function']
        self.persist_directory = self.kwargs.get('persist_directory')
        self.collection_name = self.kwargs.get('collection_name', 'faiss_index')

        if self.persist_directory and os.path.exists(
                os.path.join(self.persist_directory, f"{self.collection_name}.faiss")):
            self.store = FAISS.load_local(
                self.persist_directory,
                self.embedding_function,
                allow_dangerous_deserialization=self.allow_dangerous_deserialization
            )
        else:
            self.store = None

    @property
    def store_info(self):
        return {
            "persist_directory": self.persist_directory
        }

    def similarity_search(self, query):
        return [] if self.store is None else self.store.similarity_search(query)

    def add_texts(self, texts, metadata=None):
        if metadata is None:
            metadata = [{} for _ in range(len(texts))]
        documents = [Document(page_content=text, metadata=meta) for text, meta in zip(texts, metadata)]
        self.docs.extend(documents)
        if self.store is None:
            self.store = FAISS.from_texts([doc.page_content for doc in self.docs], self.embedding_function,
                                          metadatas=[doc.metadata for doc in self.docs])
        else:
            self.store.add_texts([doc.page_content for doc in documents], [doc.metadata for doc in documents])

        # Salva l'indice
        if self.persist_directory:
            self.store.save_local(self.persist_directory)

    def add_dataframe(self, df, source=None, additional_metadata=None, overwrite_rule=None, days_threshold=None):
        self._process_pandas_dataframe(df, source)
        if self.store is None:
            self.store = FAISS.from_documents(self.docs, self.embedding_function)
        else:
            self.store.add_documents(self.docs)

        # Salva l'indice
        if self.persist_directory:
            self.store.save_local(self.persist_directory)

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
        raise NotImplementedError("FAISS does not support document updates directly.")

    def delete_document(self, document_id):
        raise NotImplementedError("FAISS does not support document deletions directly.")

    def reset_collection(self):
        self.docs = []
        self.store = None  # Inizializza con None se non ci sono documenti
        if self.persist_directory and os.path.exists(self.persist_directory):
            os.remove(self.persist_directory)

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
            self.store = FAISS.from_documents(self.docs, self.embedding_function)
            if self.persist_directory:
                self.store.save_local(self.persist_directory)

    def manage_metadata(self, documents, source, file_type, overwrite_rule="always", days_threshold=2):
        return super().manage_metadata(documents, source, file_type, overwrite_rule, days_threshold)

    def check_and_update(self, documents, source, update_interval_days=2):
        return super().check_and_update(documents, source, update_interval_days)

    def get_all_documents(self):
        return self.docs

    def ntotal(self):
        return self.store.index.ntotal if self.store else 0
