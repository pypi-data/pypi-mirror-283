import pandas as pd
from .base_importer import BaseImporter
from datadashr.config import logger


class CSVImporter(BaseImporter):
    """
    CSVImporter is a concrete implementation of the BaseImporter class for importing CSV files.
    It provides the method to import data from a CSV file into a specified table.

    Methods:
        import_data(self, source, table_name, filters, reset):
            Imports data from a CSV file into the specified table, applying filters and resetting the table if needed.
    """

    def import_data(self, source, table_name, filters, reset):
        """
        Import data from a CSV file into the specified table.

        Args:
            source: The data source containing the CSV file path.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.

        Raises:
            ValueError: If the file path is not provided for the CSV source type.
            FileNotFoundError: If the specified file is not found.
            Exception: If there is any other error during the import process.
        """
        try:
            if source.file_path:
                data = pd.read_csv(source.file_path)
                self.connector.import_data_into_table(data, table_name, filters, reset)
            else:
                raise ValueError("File path must be provided for CSV source type")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
