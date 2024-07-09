from .base_importer import BaseImporter
from datadashr.config import *


class PandasImporter(BaseImporter):
    """
    PandasImporter is a class for importing data from a Pandas DataFrame into a specified table.

    Methods:
        import_data(self, source, table_name, filters, reset):
            Imports data from the source into the specified table.
    """

    def import_data(self, source, table_name, filters, reset):
        """
        Import data from the source into the specified table.

        Args:
            source: The source object containing the data to be imported.
            table_name (str): The name of the table to import the data into.
            filters: Filters to be applied to the data before importing.
            reset (bool): Flag to indicate whether to reset the table before importing.

        Raises:
            Exception: If an error occurs during data import.
        """
        try:
            data = source.data
            self.connector.import_data_into_table(data, table_name, filters, reset)
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e

