import os
import datetime
import pandas as pd
import polars as pl
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from datadashr.core.vector_stores.document_loader_factory import DocumentLoaderFactory
from datadashr.config import logger
import uuid


class BaseVectorStore:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.store = None

    def check_requirements(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_store(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def store_info(self):
        raise NotImplementedError("Subclasses should implement this property.")

    def filter_kwargs(self, accepted_keys):
        return {key: value for key, value in self.kwargs.items() if key in accepted_keys}

    def similarity_search(self, query):
        raise NotImplementedError("Subclasses should implement this method.")

    def add_texts(self, texts, metadata=None):
        raise NotImplementedError("Subclasses should implement this method.")

    def update_document(self, document_id, document):
        raise NotImplementedError("Subclasses should implement this method.")

    def delete_document(self, document_id):
        raise NotImplementedError("Subclasses should implement this method.")

    def delete_documents_by_metadata(self, source=None, start_date=None, end_date=None):
        raise NotImplementedError("Subclasses should implement this method.")

    def reset_collection(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def manage_metadata(self, documents, filename, file_type, overwrite_rule="always", days_threshold=2):
        updated_docs = []
        current_date = datetime.datetime.now()

        if overwrite_rule == "always":
            self.delete_documents_by_metadata(source=filename)

        for doc in documents:
            if "metadata" not in doc:
                doc.metadata = {}
            doc.metadata["source"] = filename
            doc.metadata["file_type"] = file_type
            doc.metadata["date"] = current_date.isoformat()

            if overwrite_rule == "never":
                updated_docs.append(doc)
            elif overwrite_rule == "if_older_than_days":
                existing_doc = next((d for d in updated_docs if d.metadata.get("source") == filename), None)
                if existing_doc:
                    existing_date = datetime.datetime.fromisoformat(existing_doc.metadata.get("date"))
                    if (current_date - existing_date).days > days_threshold:
                        updated_docs.remove(existing_doc)
                        updated_docs.append(doc)
                else:
                    updated_docs.append(doc)
            else:
                existing_doc = next((d for d in updated_docs if d.metadata.get("source") == filename), None)
                if existing_doc:
                    updated_docs.remove(existing_doc)
                updated_docs.append(doc)

        return updated_docs

    def check_and_update(self, documents, source, update_interval_days=2):
        updated_docs = []
        current_date = datetime.datetime.now()

        for doc in documents:
            if "metadata" not in doc:
                doc.metadata = {}
            doc.metadata["source"] = source

            last_update = doc.metadata.get("date")
            if last_update:
                last_update_date = datetime.datetime.fromisoformat(last_update)
                days_diff = (current_date - last_update_date).days
                if days_diff > update_interval_days:
                    doc.metadata["date"] = current_date.isoformat()
                    updated_docs.append(doc)
            else:
                doc.metadata["date"] = current_date.isoformat()
                updated_docs.append(doc)

        return updated_docs

    def add(self, item, source=None, file_type=None, additional_metadata=None, overwrite_rule=None, chunk_size=1000,
            chunk_overlap=0, days_threshold=None):
        if isinstance(item, pd.DataFrame):
            self.add_dataframe(item, source, additional_metadata, overwrite_rule, days_threshold)
        elif isinstance(item, str):
            self.add_texts([item], [additional_metadata])
        elif isinstance(item, list):
            self.add_texts(item, additional_metadata)
        else:
            raise ValueError("Unsupported item type for adding to vector store.")

    def add_document(self, document_path, chunk_size=1000, chunk_overlap=0, overwrite_rule="always", days_threshold=2):
        if not document_path or not os.path.exists(document_path):
            raise FileNotFoundError(f"Document path {document_path} does not exist.")

        filename = os.path.basename(document_path)
        file_type = os.path.splitext(document_path)[1].lower()
        loader = DocumentLoaderFactory.get_loader(document_path)
        self.documents = loader.load()
        self.text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.docs = self.text_splitter.split_documents(self.documents)

        self.docs = self.manage_metadata(self.docs, filename, file_type, overwrite_rule, days_threshold)
        self.add_texts([doc.page_content for doc in self.docs], metadata=[doc.metadata for doc in self.docs])

    def add_from_directory(self, directory_path, chunk_size=1000, chunk_overlap=0, overwrite_rule="always",
                           days_threshold=2):
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory path {directory_path} does not exist.")

        for filename in os.listdir(directory_path):
            document_path = os.path.join(directory_path, filename)
            try:
                self.add_document(document_path, chunk_size, chunk_overlap, overwrite_rule, days_threshold)
            except ValueError as e:
                print(f"Skipping {document_path}: {e}")

    def add_dataframe(self, df, source, dataframe_type='pandas', additional_metadata=None, overwrite_rule="always",
                      days_threshold=2):
        logger.info(f"Adding dataframe '{source}' of type '{dataframe_type}' to the vectorstore.")
        if dataframe_type == 'polars' and isinstance(df, pd.DataFrame):
            raise ValueError("Provided dataframe is a Pandas DataFrame but 'polars' type was specified.")
        elif dataframe_type == 'pandas' and isinstance(df, pl.DataFrame):
            raise ValueError("Provided dataframe is a Polars DataFrame but 'pandas' type was specified.")

        if dataframe_type == 'pandas':
            documents = self._process_pandas_dataframe(df, source, additional_metadata)
        elif dataframe_type == 'polars':
            documents = self._process_polars_dataframe(df, source, additional_metadata)
        else:
            raise ValueError("Unsupported dataframe type. Please provide a Pandas or Polars DataFrame.")

        documents = self.manage_metadata(documents, source, dataframe_type, overwrite_rule, days_threshold)
        logger.info(f"Adding {len(documents)} documents to the vectorstore.")
        self.add_texts([doc.page_content for doc in documents], metadata=[doc.metadata for doc in documents])

    def _process_pandas_dataframe(self, df, source, additional_metadata):
        logger.info(f"Processing pandas dataframe '{source}' with {len(df)} rows.")
        documents = []
        for _, row in df.iterrows():
            text = ' '.join([f"{col}: {val}" for col, val in row.items()])
            metadata = self._generate_metadata(row, source, 'pandas', additional_metadata)
            doc_id = str(uuid.uuid4())
            metadata['id'] = doc_id
            doc = Document(page_content=text, metadata=metadata)
            logger.info(f"Adding document with metadata: {metadata}")
            documents.append(doc)
        return documents

    def _process_polars_dataframe(self, df, source, additional_metadata):
        logger.info(f"Processing polars dataframe '{source}' with {len(df)} rows.")
        documents = []
        for row in df.iter_rows(named=True):
            text = ' '.join([f"{col}: {val}" for col, val in row.items()])
            metadata = self._generate_metadata(row, source, 'polars', additional_metadata)
            doc_id = str(uuid.uuid4())
            metadata['id'] = doc_id
            documents.append(Document(page_content=text, metadata=metadata))
        return documents

    def _generate_metadata(self, row, source, dataframe_type, additional_metadata, document_hash=None):
        metadata = {'source': source, 'dataframe_type': dataframe_type, 'document_hash': document_hash}
        if additional_metadata:
            metadata.update(additional_metadata)

        filtered_metadata = {k: v for k, v in metadata.items() if self._is_supported_metadata(v)}

        row_metadata = {f'col_{k}': v for k, v in row.items() if self._is_supported_metadata(v)}
        filtered_metadata.update(row_metadata)

        return filtered_metadata

    @staticmethod
    def _is_supported_metadata(value):
        return isinstance(value, (str, int, float, bool)) and (not isinstance(value, str) or len(value) < 100)

    def get_documents(self, limit=10, offset=0):
        raise NotImplementedError("Subclasses should implement this method.")
