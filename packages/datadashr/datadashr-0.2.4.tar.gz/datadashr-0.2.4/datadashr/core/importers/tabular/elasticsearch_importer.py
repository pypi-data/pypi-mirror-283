import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from .base_importer import BaseImporter
from datadashr.config import *


class ElasticsearchImporter(BaseImporter):
    """
    ElasticsearchImporter is a concrete implementation of the BaseImporter class for importing data from Elasticsearch.
    It provides the method to import data from an Elasticsearch index into a specified table.

    Methods:
        import_data(self, source, table_name, filters, reset):
            Imports data from an Elasticsearch index into the specified table, applying filters
            and resetting the table if needed.
    """

    def import_data(self, source, table_name, filters, reset):
        """
        Import data from an Elasticsearch index into the specified table.

        Args:
            source: The data source containing the Elasticsearch connection details and index.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.

        Raises:
            Exception: If there is any error during the import process.
        """
        try:
            if source.username and source.password:
                es = Elasticsearch(source.host, http_auth=(source.username, source.password))
            else:
                es = Elasticsearch(source.host)

            query_body = {"query": {"match_all": {}}}  # Default query body

            if filters:
                query_body = {
                    "query": {
                        "bool": {
                            "must": [{"match": {key: value}} for key, value in filters.items()]
                        }
                    }
                }

            data = [hit["_source"] for hit in scan(es, index=source.index, query=query_body)]
            df = pd.DataFrame(data)
            self.connector.import_data_into_table(df, table_name, filters, reset)
            es.close()
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e
