import duckdb
import json
import hashlib
from datetime import datetime, timedelta
from datadashr.core.utilities import Utilities
from datadashr.config import logger


class CacheManager:
    """
    CacheManager handles the caching of database query results using DuckDB.

    Methods:
    - __init__(self, db_folder, verbose=False): Initialize the CacheManager with the specified database folder and verbosity.
    - _create_cache_table(self): Create the cache table if it does not exist.
    - _verify_and_recreate_table(self): Verify the cache table structure and recreate it if it differs from the defined structure.
    - _generate_key(self, query, tables, fields): Generate a unique key for caching based on the query, tables, and fields.
    - get(self, query, tables, fields): Retrieve a cached response if it exists.
    - set(self, query, tables, fields, response): Cache the response of a query.
    - clean_old_entries(self): Remove cache entries older than a specified threshold.
    - clean_cache(self): Clear all entries from the cache.
    """

    def __init__(self, db_folder, delete_cache=False, verbose=False):
        """
        Initialize the CacheManager with the specified database folder and verbosity.
        :param db_folder: Path to the folder containing the DuckDB database file.
        :param verbose: Enable verbose logging if True.
        """
        self.db_folder = db_folder
        self.db_file = f"{db_folder}/cache.duckdb"
        self.verbose = verbose
        self.ut = Utilities(self.verbose)
        self._verify_and_recreate_table()
        if delete_cache:
            self.clean_cache()

    def _create_cache_table(self):
        """
        Create the cache table if it does not exist.
        """
        if self.verbose:
            logger.info("Creating cache table")
        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS cache (
                        key VARCHAR PRIMARY KEY,
                        query VARCHAR,
                        response VARCHAR,
                        timestamp TIMESTAMP
                    )
                ''')
                if self.verbose:
                    logger.info("Cache table created successfully")
        except Exception as e:
            logger.error(f"Error creating cache table: {e}")

    def _verify_and_recreate_table(self):
        """
        Verify the cache table structure and recreate it if it differs from the defined structure.
        """
        expected_columns = {
            "key": "VARCHAR",
            "query": "VARCHAR",
            "response": "VARCHAR",
            "timestamp": "TIMESTAMP"
        }

        try:
            with duckdb.connect(self.db_file) as conn:
                # Get the existing table structure
                result = conn.execute("DESCRIBE cache").fetchall()
                existing_columns = {row[0]: row[1] for row in result}
                if self.verbose:
                    logger.info(f"Existing cache table columns: {existing_columns}")
                    logger.info(f"Expected cache table columns: {expected_columns}")

                if existing_columns != expected_columns:
                    if self.verbose:
                        logger.info("Cache table structure differs from the expected structure, recreating the table")
                    conn.execute("DROP TABLE IF EXISTS cache")
                    self._create_cache_table()
                elif self.verbose:
                    logger.info("Cache table structure matches the expected structure")
        except Exception as e:
            if self.verbose:
                logger.error(f"Error verifying/recreating cache table: {e}")
            self._create_cache_table()

    def _generate_key(self, query, tables, fields):
        """
        Generate a unique key for caching based on the query, tables, and fields.
        :param query: The SQL query string.
        :param tables: List of table names involved in the query.
        :param fields: Dictionary of table names to lists of field names involved in the query.
        :return: A SHA-256 hash string representing the cache key.
        """
        try:
            # Convert table and field names to lowercase and sort them
            tables_str = json.dumps(sorted([table.lower() for table in tables]), sort_keys=True)
            fields_str = json.dumps(
                {table.lower(): sorted([field.lower() for field in fields[table]]) for table in fields},
                sort_keys=True
            )
            combined = f"{query.lower()}-{tables_str}-{fields_str}"
            if self.verbose:
                logger.info(f"Generating key for tables_str: {tables_str}")
                logger.info(f"Generating key for fields_str: {fields_str}")
                logger.info(f"Generating key for: {combined}")
                logger.info(f"Generated key: {hashlib.sha256(combined.encode('utf-8')).hexdigest()}")
            return hashlib.sha256(combined.encode('utf-8')).hexdigest()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error generating key: {e}")
            return None

    def get(self, query, tables, fields):
        """
        Retrieve a cached response if it exists.
        :param query: The SQL query string.
        :param tables: List of table names involved in the query.
        :param fields: Dictionary of table names to lists of field names involved in the query.
        :return: The cached response as a JSON object, or None if not found.
        """
        try:
            self.clean_old_entries()
            key = self._generate_key(query, tables, fields)
            with duckdb.connect(self.db_file) as conn:
                if result := conn.execute(
                        'SELECT response FROM cache WHERE key = ?', (key,)
                ).fetchone():
                    return result[0]
                return None
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting cache: {e}")
            return None

    def set(self, query, tables, fields, response):
        """
        Cache the response of a query.
        :param query: The SQL query string.
        :param tables: List of table names involved in the query.
        :param fields: Dictionary of table names to lists of field names involved in the query.
        :param response: The response to cache.
        """
        try:
            key = self._generate_key(query, tables, fields)
            timestamp = datetime.now()
            with duckdb.connect(self.db_file) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO cache (key, query, response, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (key, query.lower(), json.dumps(response), timestamp))

            if self.verbose:
                # verify that the cache was set correctly
                with duckdb.connect(self.db_file) as conn:
                    if result := conn.execute(
                            'SELECT response FROM cache WHERE key = ?', (key,)
                    ).fetchone():
                        logger.info(f"Cache set successfully for key: {key}")
                    else:
                        logger.error(f"Error setting cache for key: {key}")
        except Exception as e:
            logger.error(f"Error setting cache: {e}")

    def clean_old_entries(self):
        """
        Remove cache entries older than a specified threshold.
        :param days: The number of days to keep entries before they are considered old.
        """
        try:
            threshold = datetime.now() - timedelta(days=30)
            with duckdb.connect(self.db_file) as conn:
                conn.execute('DELETE FROM cache WHERE timestamp < ?', (threshold,))
        except Exception as e:
            if self.verbose:
                logger.error(f"Error cleaning cache: {e}")

    def clean_cache(self):
        """
        Clear all entries from the cache.
        """
        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('DELETE FROM cache')
        except Exception as e:
            if self.verbose:
                logger.error(f"Error cleaning cache: {e}")

    def get_cache_history(self):
        """
        Retrieve the cache history.
        :return: The cache history as a JSON object with column-value format.
        """
        try:
            with duckdb.connect(self.db_file) as conn:
                results = conn.execute('SELECT * FROM cache').fetchall()

                # Define the column names
                columns = ['hash', 'request', 'response', 'timestamp']

                # Transform the results into column-value format
                cache_history = []
                for row in results:
                    record = {columns[i]: row[i] for i in range(len(columns))}
                    cache_history.append(record)

                return json.dumps(cache_history, default=str)  # Convert datetime to string
        except Exception as e:
            if self.verbose:
                logger.error(f"Error getting cache history: {e}")
            return None

    def delete_by_hash(self, hash):
        """
        Delete a cache entry by hash.
        :param hash: The hash of the cache entry to delete.
        """
        try:
            with duckdb.connect(self.db_file) as conn:
                conn.execute('DELETE FROM cache WHERE hash = ?', (hash,))
        except Exception as e:
            if self.verbose:
                logger.error(f"Error deleting cache entry: {e}")

            return False

        return True
