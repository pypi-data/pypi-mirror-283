import os
import pandas as pd
import polars as pl
from langchain_community.document_loaders import TextLoader, CSVLoader, PyMuPDFLoader, DataFrameLoader, \
    PolarsDataFrameLoader, UnstructuredExcelLoader, Docx2txtLoader, NotionDBLoader, EverNoteLoader


class DocumentLoaderFactory:
    @staticmethod
    def get_loader(document):
        # dataframe
        if isinstance(document, pd.DataFrame):
            return DataFrameLoader(document)
        # polars dataframe
        elif isinstance(document, pl.DataFrame):
            return PolarsDataFrameLoader(document)
        # txt
        elif isinstance(document, str) and document.endswith('.txt'):
            return TextLoader(document)
        # csv
        elif isinstance(document, str) and document.endswith('.csv'):
            return CSVLoader(document)
        # pdf
        elif isinstance(document, str) and document.endswith('.pdf'):
            return PyMuPDFLoader(document)
        # notiondb
        elif isinstance(document, str) and document.endswith('.notiondb'):
            return NotionDBLoader(document)
        # evernote
        elif isinstance(document, str) and document.endswith('.evernote'):
            return EverNoteLoader(document)
        # excel
        elif isinstance(document, str) and (document.endswith('.xls') or document.endswith('.xlsx')):
            return UnstructuredExcelLoader(document)
        # docx
        elif isinstance(document, str) and document.endswith('.docx'):
            return Docx2txtLoader(document)

        # Aggiungere ulteriori controlli per altri tipi di file e relativi loader
        else:
            raise ValueError(f"Unsupported document type: {document}")
