import pyarrow.parquet as pq
from .base_importer import BaseImporter
from datadashr.config import *


class ParquetImporter(BaseImporter):
    """
    ParquetImporter is a concrete implementation of the BaseImporter class for importing data from Parquet files.
    It provides the method to import data from a Parquet file into a specified table.

    Methods:
        import_data(self, source, table_name, filters, reset):
            Imports data from a Parquet file into the specified table, applying filters
            and resetting the table if needed.
    """

    def import_data(self, source, table_name, filters, reset):
        """
        Import data from a Parquet file into the specified table.

        Args:
            source: The data source containing the Parquet file path.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.

        Raises:
            FileNotFoundError: If the specified file is not found.
            Exception: If there is any other error during the import process.
        """
        try:
            data = pq.read_table(source.file_path).to_pandas()
            self.connector.import_data_into_table(data, table_name, filters, reset)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e
