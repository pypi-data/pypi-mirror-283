from .base_importer import BaseImporter
from datadashr.config import *


class PolarsImporter(BaseImporter):
    """
    PolarsImporter is a concrete implementation of the BaseImporter class for importing data using Polars DataFrame.
    It provides the method to import data from a Polars DataFrame into a specified table.

    Methods:
        import_data(self, source, table_name, filters, reset):
            Imports data from a Polars DataFrame into the specified table, applying filters
            and resetting the table if needed.
    """

    def import_data(self, source, table_name, filters, reset):
        """
        Import data from a Polars DataFrame into the specified table.

        Args:
            source: The data source containing the Polars DataFrame.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.

        Raises:
            Exception: If there is any error during the import process.
        """
        try:
            data = source.data.to_pandas()
            self.connector.import_data_into_table(data, table_name, filters, reset)
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e
