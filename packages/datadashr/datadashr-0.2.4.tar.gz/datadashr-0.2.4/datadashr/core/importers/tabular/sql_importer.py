import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from .base_importer import BaseImporter
from datadashr.config import *


class SQLImporter(BaseImporter):
    """
    SQLImporter is a concrete implementation of the BaseImporter class for importing data from SQL databases.
    It provides methods to build the connection string and import data from a SQL database into a specified table.

    Methods:
        build_connection_string(self, sql_config):
            Builds the connection string for the SQL database.

        import_data(self, source, table_name, filters, reset):
            Imports data from a SQL database into the specified table, applying filters
            and resetting the table if needed.

        _extracted_from_import_data(self, source, table_name, filters, reset):
            Helper method to execute the import data process.
    """

    @staticmethod
    def build_connection_string(sql_config):
        """
        Build the connection string for the SQL database.

        Args:
            sql_config: The SQL configuration object containing connection details.

        Returns:
            str: The connection string for the SQL database.
        """
        return f"{sql_config.dialect}+{sql_config.driver}://" \
               f"{sql_config.username}:{sql_config.password}@" \
               f"{sql_config.host}:{sql_config.port}/" \
               f"{sql_config.database}"

    def import_data(self, source, table_name, filters, reset):
        """
        Import data from a SQL database into the specified table.

        Args:
            source: The data source containing the SQL connection details and query.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.

        Raises:
            SQLAlchemyError: If there is an error related to SQLAlchemy during the import process.
            Exception: If there is any other error during the import process.
        """
        try:
            self._extracted_from_import_data(source, table_name, filters, reset)
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")

    def _extracted_from_import_data(self, source, table_name, filters, reset):
        """
        Helper method to execute the import data process.

        Args:
            source: The data source containing the SQL connection details and query.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.
        """
        connection_string = self.build_connection_string(source.connection_string)
        engine = create_engine(connection_string)
        query = source.query or f"SELECT * FROM {table_name.replace('_sql', '')}"

        if filters:
            filter_conditions = " AND ".join([f"{key} = '{value}'" for key, value in filters.items()])
            query += f" WHERE {filter_conditions}"

        data = pd.read_sql(query, engine)
        self.connector.import_data_into_table(data, table_name, filters, reset)
        engine.dispose()
