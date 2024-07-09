import duckdb
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Hashable, List, Tuple
from datadashr.config import *
from datadashr.core.importers.tabular.models.import_data_config import ImportDataConfig
from datadashr.core.importers.tabular.pandas_importer import PandasImporter
from datadashr.core.importers.tabular.polars_importer import PolarsImporter
from datadashr.core.importers.tabular.csv_importer import CSVImporter
from datadashr.core.importers.tabular.sql_importer import SQLImporter
from datadashr.core.importers.tabular.elasticsearch_importer import ElasticsearchImporter
from datadashr.core.importers.tabular.parquet_importer import ParquetImporter
from datadashr.core.vector_stores import VectorStore
from datadashr.core.embeddings import Embedding


class Connector:
    """
    The Connector class manages data imports, database interactions, and relationship definitions within DuckDB.
    It supports various data sources including Pandas, Polars, CSV, SQL, Elasticsearch, and Parquet.

    Attributes:
    IMPORTER_CLASSES (dict): A dictionary mapping source types to their corresponding importer classes.
    """

    IMPORTER_CLASSES = {
        'pandas': PandasImporter,
        'polars': PolarsImporter,
        'csv': CSVImporter,
        'sql': SQLImporter,
        'elasticsearch': ElasticsearchImporter,
        'parquet': ParquetImporter,
    }

    def __init__(self, db_path: str = DUCKDB_PATH, reset: bool = False, verbose: bool = False):
        """
        Initializes the Connector instance.

        Args:
        db_path (str): Path to the DuckDB database file.
        reset (bool): If True, a new in-memory database is used.
        verbose (bool): If True, enables verbose logging.
        """
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = duckdb.connect(':memory:') if reset else duckdb.connect(db_path)
        self.conn.execute("SET memory_limit = '20GB'")
        self.conn.execute("SET threads TO 5")
        self.conn.execute("SET enable_progress_bar = true")

        self.sources = {}
        self.source_type = None
        self.relations = {}
        self.descriptions = {}
        self.tables = []
        self.verbose = verbose

    @staticmethod
    def connector_type():
        """
        Returns the type of the connector.
        """
        return 'duckdb'

    def return_tables(self):
        """
        Returns the list of tables.
        """
        return self.tables

    def import_data(self, import_data: Dict[str, Any], reset: bool = False, reset_db: bool = False, **kwargs):
        """
        Imports data into the DuckDB database.

        Args:
        import_data (Dict[str, Any]): Dictionary containing the data and its configuration for import.
        reset (bool): If True, resets the data.
        reset_db (bool): If True, resets the database.
        """
        if reset_db:
            self.reset_database()

        validated_data = ImportDataConfig(**import_data)

        for source in validated_data.sources:
            source_name = source.source_name.lower()
            self.source_type = source_type = source.source_type
            description = source.description.lower() if source.description else "No description available"
            table_name = f"{source_name}_{source_type}" if (source_type in
                                                            ['polars', 'pandas', 'csv', 'parquet']) else source_name
            if hasattr(source, 'delete_table') and source.delete_table:
                self.delete_table(table_name)

            self.tables.append(table_name)
            self.descriptions[table_name] = description
            if self.verbose:
                logger.info(f"Description {self.descriptions[table_name]} - {description}")

            if importer_class := self.IMPORTER_CLASSES.get(source_type):
                importer = importer_class(self)
                filter_conditions = source.filter
                try:
                    importer.import_data(source, table_name, filter_conditions, reset)
                except Exception as e:
                    logger.error(f"Failed to import {source_name} of type {source_type}: {e}")
            else:
                logger.error(f"Unsupported source type: {source_type}")

        if 'mapping' in import_data:
            for key, tables in import_data['mapping'].items():
                for i in range(len(tables) - 1):
                    try:
                        self.define_relation(
                            tables[i]['source'].lower(), tables[i]['field'].lower(),
                            tables[i + 1]['source'].lower(), tables[i + 1]['field'].lower()
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to define relation between {tables[i]['source']} "
                            f"and {tables[i + 1]['source']}: {e}")
        else:
            self.auto_define_relations()

        if self.verbose:
            logger.info(f"Relations defined before creating structure table: {self.relations}")

        self.create_relation_structure_table()
        self.create_combined_dataframe_and_save_to_vector(import_data, **kwargs)

    def reset_database(self):
        """
        Resets the DuckDB database by dropping all tables.
        """
        tables = self.conn.execute("SHOW TABLES").fetchall()
        for table in tables:
            self.conn.execute(f"DROP TABLE IF EXISTS {table[0]}")

        self.sources = {}
        self.relations = {}

    def register_data(self, source_name: str, data: pd.DataFrame):
        """
        Registers a Pandas DataFrame as a table in the DuckDB database.

        Args:
        source_name (str): The name of the source table.
        data (pd.DataFrame): The data to be registered.
        """
        self.sources[source_name] = data
        if source_name in self.conn.execute("SHOW TABLES").fetchdf()['name'].str.lower().tolist():
            for d in data.itertuples(index=False):
                self.conn.execute(f"INSERT OR REPLACE INTO {source_name} VALUES {tuple(d)}")
        else:
            self.conn.execute(f"CREATE TABLE {source_name} AS SELECT * FROM data")

    def define_relation(self, source1: str, key1: str, source2: str, key2: str):
        """
        Defines a relation between two tables based on their columns.

        Args:
        source1 (str): The first table.
        key1 (str): The column in the first table.
        source2 (str): The second table.
        key2 (str): The column in the second table.
        """
        if source1 not in self.relations:
            self.relations[source1] = []
        self.relations[source1].append((source2, key1, key2))

        if source2 not in self.relations:
            self.relations[source2] = []
        self.relations[source2].append((source1, key2, key1))
        if self.verbose:
            logger.info(
                f"Defined relation: {source1}.{key1} -> {source2}.{key2} and {source2}.{key2} -> {source1}.{key1}")

    def auto_define_relations(self):
        """
        Automatically defines relations between tables based on common column names.
        """
        source_names = list(self.sources.keys())
        for i, source1 in enumerate(source_names):
            for source2 in source_names[i + 1:]:
                columns1 = set(self.conn.execute(f"PRAGMA table_info('{source1}')").fetchdf()['name'])
                columns2 = set(self.conn.execute(f"PRAGMA table_info('{source2}')").fetchdf()['name'])
                common_keys = columns1.intersection(columns2)
                for key in common_keys:
                    try:
                        self.define_relation(source1, key, source2, key)
                    except Exception as e:
                        logger.error(f"Failed to define relation for key {key} between {source1} and {source2}: {e}")

    def create_relation_structure_table(self):
        """
        Creates a table in the DuckDB database to store the defined relations between tables.
        """
        self.conn.execute("DROP TABLE IF EXISTS relation_structure")
        self.conn.execute(
            "CREATE TABLE relation_structure (source1 VARCHAR, key1 VARCHAR, source2 VARCHAR, key2 VARCHAR)")

        if self.verbose:
            logger.info(f"Inserting relations into relation_structure: {self.relations}")

        for source1, rels in self.relations.items():
            for (source2, key1, key2) in rels:
                try:
                    if self.verbose:
                        logger.info(f"Inserting relation: {source1}, {key1}, {source2}, {key2}")
                    self.conn.execute("INSERT INTO relation_structure VALUES (?, ?, ?, ?)",
                                      (source1, key1, source2, key2))
                except Exception as e:
                    logger.error(f"Failed to insert relation into relation_structure: {e}")

        if self.verbose:
            logger.info("Relation structure table created")
            logger.info(f"Relation structure: {self.relations}")

            relation_count = self.conn.execute("SELECT COUNT(*) FROM relation_structure").fetchone()[0]
            logger.info(f"Number of relations in relation_structure: {relation_count}")
            relations_df = self.conn.execute("SELECT * FROM relation_structure").fetchdf()
            logger.info(f"Content of relation_structure: {relations_df}")

    def execute_query(self, query: str) -> List[Tuple]:
        """
        Executes a SQL query on the DuckDB database.

        Args:
        query (str): The SQL query to execute.

        Returns:
        List[Tuple]: The result of the query.
        """
        try:
            return self.conn.execute(query).fetchall()
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            return []

    def export_database(self, file_path: str):
        """
        Exports the DuckDB database to a specified file.

        Args:
        file_path (str): The path to the export file.
        """
        try:
            self.conn.execute(f"EXPORT DATABASE '{file_path}'")
        except Exception as e:
            logger.error(f"Failed to export database: {e}")

    @staticmethod
    def get_column_types(data: pd.DataFrame) -> dict[Hashable, str]:
        """
        Determines the column types for a given Pandas DataFrame.

        Args:
        data (pd.DataFrame): The data to analyze.

        Returns:
        dict[Hashable, str]: A dictionary mapping column names to DuckDB-compatible data types.
        """
        column_types = {}
        for column, dtype in data.dtypes.items():
            if pd.api.types.is_integer_dtype(dtype):
                column_types[column] = 'BIGINT' if data[column].max() > 2147483647 else 'INTEGER'
            elif pd.api.types.is_float_dtype(dtype):
                column_types[column] = 'DOUBLE'
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_types[column] = 'TIMESTAMP'
            else:
                column_types[column] = 'VARCHAR'
        return column_types

    @staticmethod
    def apply_filters(data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Applies filters to a Pandas DataFrame.

        Args:
        data (pd.DataFrame): The data to filter.
        filters (Dict[str, Any]): A dictionary of filters to apply.

        Returns:
        pd.DataFrame: The filtered data.
        """
        for key, value in filters.items():
            data = data[data[key] == value]
        return data

    def import_data_into_table(self, data: pd.DataFrame, table_name: str, filters: Dict[str, Any], reset: bool):
        """
        Imports data into a specified table in the DuckDB database.

        Args:
        data (pd.DataFrame): The data to import.
        table_name (str): The name of the table.
        filters (Dict[str, Any]): Filters to apply to the data.
        reset (bool): If True, resets the table before importing.
        """
        try:
            data.columns = data.columns.str.lower()
            data['dt_insert'] = datetime.now()

            if filters:
                data = self.apply_filters(data, filters)

            if 'id' not in data.columns:
                data.insert(0, 'id', range(1, 1 + len(data)))

            if reset:
                self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")

            column_types = self.get_column_types(data)

            if table_name in self.conn.execute("SHOW TABLES").fetchdf()['name'].str.lower().tolist():
                columns = ', '.join(data.columns)
                placeholders = ', '.join(['?'] * len(data.columns))
                insert_query = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
                for d in data.itertuples(index=False):
                    self.conn.execute(insert_query, tuple(d))
            else:
                columns_with_types = ', '.join([f"{col} {col_type}" for col, col_type in column_types.items()])
                create_query = f"CREATE TABLE {table_name} ({columns_with_types}, PRIMARY KEY(id))"
                self.conn.execute(create_query)
                self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM data")
        except Exception as e:
            logger.error(f"Failed to import data into {table_name}: {e}")

    def existing_tables(self) -> set:
        """
        Retrieves the set of existing tables in the DuckDB database.

        Returns:
        set: The set of existing table names.
        """
        existing_tables = {table[0] for table in self.conn.execute("SHOW TABLES").fetchall()}
        existing_tables.discard('relation_structure')

        sources = self.tables

        if all(source in existing_tables for source in sources):
            if self.verbose:
                logger.info(f"return sources: {sources}")
            return set(sources)
        else:
            logger.info(f"return existing_tables: {existing_tables}")
            return existing_tables or set()

    def table_info(self) -> Dict[str, pd.DataFrame]:
        """
        Retrieves information about the columns of each table in the DuckDB database.

        Returns:
        Dict[str, pd.DataFrame]: A dictionary mapping table names to their column information.
        """
        table_info = {
            table: self.conn.execute(f"PRAGMA table_info('{table}')").fetchdf()
            for table in self.existing_tables()
        }
        return table_info or {}

    def get_table_description(self, table_name: str) -> str:
        """
        Retrieves the description of a specified table.

        Args:
        table_name (str): The name of the table.

        Returns:
        str: The description of the table.
        """
        return self.descriptions.get(table_name, "No description available")

    def get_all_table_descriptions(self) -> Dict[str, str]:
        """
        Retrieves the descriptions of all tables.

        Returns:
        Dict[str, str]: A dictionary mapping table names to their descriptions.
        """
        return self.descriptions

    def delete_table(self, table_name: str):
        """
        Deletes a specified table from the DuckDB database.

        Args:
        table_name (str): The name of the table to delete.
        """
        try:
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            if table_name in self.tables:
                self.tables.remove(table_name)
            if table_name in self.descriptions:
                del self.descriptions[table_name]
            logger.info(f"Table {table_name} deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete table {table_name}: {e}")

    def delete_all_tables(self):
        """
        Deletes all tables from the DuckDB database.
        """
        for table in self.existing_tables():
            self.delete_table(table)
        logger.info("All tables deleted successfully.")

    def create_combined_dataframe_and_save_to_vector(self, import_data: Dict[str, Any], **kwargs):
        """
        Creates a combined DataFrame from multiple sources and saves it to a vector store.

        Args:
        import_data (Dict[str, Any]): Dictionary containing the data and its configuration for import.
        """
        combined_table_name = 'combined_temp_table'
        try:
            # Step 1: Read the data from each source
            data_sources = {}
            for source in import_data['sources']:
                table_name = source['source_name'].lower()
                data = source['data']
                data_sources[table_name] = data

            # Step 2: Ensure the types of columns used for merging are consistent
            for key, mappings in import_data['mapping'].items():
                for mapping in mappings:
                    source = mapping['source'].lower()
                    field = mapping['field']
                    if data_sources[source][field].dtype != 'object':
                        data_sources[source][field] = data_sources[source][field].astype('object')

            # Step 3: Merge the data based on the specified mappings
            combined_df = None
            for key, mappings in import_data['mapping'].items():
                source_1 = mappings[0]['source'].lower()
                field_1 = mappings[0]['field']
                source_2 = mappings[1]['source'].lower()
                field_2 = mappings[1]['field']

                if combined_df is None:
                    combined_df = pd.merge(
                        data_sources[source_1],
                        data_sources[source_2],
                        left_on=field_1,
                        right_on=field_2,
                        how='outer',
                        suffixes=('_' + source_1, '_' + source_2)
                    )
                else:
                    combined_df = pd.merge(
                        combined_df,
                        data_sources[source_2],
                        left_on=field_1,
                        right_on=field_2,
                        how='outer',
                        suffixes=('', '_' + source_2)
                    )

            # Step 4: Handle additional merges if there are more than two sources for a key
            for key, mappings in import_data['mapping'].items():
                for i in range(2, len(mappings)):
                    source_next = mappings[i]['source'].lower()
                    field_next = mappings[i]['field']
                    combined_df = pd.merge(
                        combined_df,
                        data_sources[source_next],
                        left_on=field_1,
                        right_on=field_next,
                        how='outer',
                        suffixes=('', '_' + source_next)
                    )

            # Step 5: Register the combined dataframe in DuckDB and save to vector
            self.conn.execute(f"DROP TABLE IF EXISTS {combined_table_name}")
            self.conn.register('combined_df', combined_df)
            self.conn.execute(f"CREATE TABLE {combined_table_name} AS SELECT * FROM combined_df")

            # Log the combined data
            if self.verbose:
                logger.info(f"Combined data: {combined_df.head()}")

            # Vectorize the data and save it
            self.vectorize_data(combined_df, **kwargs)

            # Clean up by dropping the temporary table
            self.conn.execute(f"DROP TABLE IF EXISTS {combined_table_name}")

        except Exception as e:
            logger.error(f"Failed during combined dataframe creation: {e}")
            if combined_table_name:
                self.conn.execute(f"DROP TABLE IF EXISTS {combined_table_name}")

    def create_temporary_table(self, import_data: Dict[str, Any]):
        """
        Creates a temporary table in DuckDB for storing combined data.

        Args:
        import_data (Dict[str, Any]): Dictionary containing the data and its configuration for import.
        """
        combined_columns = set()
        for source in import_data['sources']:
            table_name = source['source_name'].lower()
            data = source['data'] if 'data' in source else self.conn.execute(f"SELECT * FROM {table_name}").fetchdf()
            columns = {f"{col}_{table_name}" for col in data.columns}
            combined_columns.update(columns)
            logger.debug(f"Columns of {table_name} after renaming: {data.columns.tolist()}")

        columns_with_types = ', '.join([f"{col} VARCHAR" for col in combined_columns])
        create_query = f"CREATE TABLE combined_temp_table ({columns_with_types})"
        self.conn.execute(create_query)

    def populate_temporary_table(self, import_data: Dict[str, Any]):
        """
        Populates the temporary table with data from the specified sources.

        Args:
        import_data (Dict[str, Any]): Dictionary containing the data and its configuration for import.
        """
        for source in import_data['sources']:
            table_name = source['source_name'].lower()
            data = source['data'] if 'data' in source else self.conn.execute(f"SELECT * FROM {table_name}").fetchdf()

            # Rename columns to avoid conflicts
            renamed_columns = {col: f"{col}_{table_name}" for col in data.columns}
            data = data.rename(columns=renamed_columns)

            # Ensure all columns are present in the temporary table
            temp_table_columns = self.conn.execute("PRAGMA table_info('combined_temp_table')").fetchdf()[
                'name'].tolist()
            missing_columns = set(temp_table_columns) - set(data.columns)

            # Add missing columns with None values
            for col in missing_columns:
                data[col] = None

            # Select columns in the order of the temporary table
            data = data[temp_table_columns]

            # Insert data into the temporary table
            self.conn.register('data', data)
            insert_query = f"INSERT INTO combined_temp_table SELECT * FROM data"
            self.conn.execute(insert_query)

            if self.verbose:
                logger.debug(f"Data inserted into combined_temp_table: {data.head()}")

    @staticmethod
    def vectorize_data(combined_df: pd.DataFrame, **kwargs):
        """
        Vectorizes the combined DataFrame and saves it to a vector store.

        Args:
        combined_df (pd.DataFrame): The combined data to be vectorized.
        kwargs (dict): Additional keyword arguments for vectorization.
        """
        embedding = kwargs.get('embedding', {})
        vector_store = kwargs.get('vector_store', {})
        emb = Embedding(embedding_type=embedding.get('embedding_type', 'fastembed'),
                        model_name=embedding.get('model_name', None),
                        api_key=embedding.get('api_key', None))

        vector = VectorStore(store_type=vector_store.get('store_type', 'chromadb'),
                             persist_directory=vector_store.get('persist_directory', VECTOR_DIR),
                             collection_name=vector_store.get('collection_name', 'datadashr'),
                             api_key=vector_store.get('api_key', None),
                             embedding_function=emb.get_embedding())
        vector.add(combined_df, chunk_size=1000, chunk_overlap=0, overwrite_rule="always")
        logger.info("Combined data saved to vector: combined_df")
