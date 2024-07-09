"""
Author: Fabio Cantone
Email: dev@datadashr.com
Date: 2024-07-06
Version: 0.2.4
License: Custom License (Non-Commercial Use)
"""

import os
import json
import yaml

from typing import Any, Optional
from datadashr.config import logger, CACHE_DIR, CHART_DIR, LOG_DIR, DUCKDB_PATH, VECTOR_DIR


def find_settings_file(filename: str) -> Optional[str]:
    """
    Searches for the specified settings file by traversing up the directory tree.

    Args:
        filename (str): The name of the settings file to find.

    Returns:
        Optional[str]: The path to the found settings file, or None if not found.
    """
    current_dir = os.path.abspath(os.getcwd())
    while current_dir != os.path.dirname(current_dir):
        potential_path = os.path.join(current_dir, filename)
        if os.path.exists(potential_path):
            return potential_path
        current_dir = os.path.dirname(current_dir)
    return None


def recursive_update(original: dict, updates: dict) -> dict:
    """
    Recursively updates a dictionary with another dictionary.

    Args:
        original (dict): The original dictionary to be updated.
        updates (dict): The dictionary with updates.

    Returns:
        dict: The updated dictionary.
    """
    for key, value in updates.items():
        if isinstance(value, dict) and key in original:
            original[key] = recursive_update(original.get(key, {}), value)
        else:
            original[key] = value
    return original


class Settings:
    """
    Settings class manages the configuration settings for the DataDashr project.
    It supports loading settings from JSON or YAML files, or from keyword arguments.

    Attributes:
        path (str): The root path of the project.
        cache_dir (str): The directory for caching data.
        chart_dir (str): The directory for storing charts.
        log_dir (str): The directory for log files.
        db_path (str): The path to the DuckDB database.
        vector_db_path (str): The directory for storing vector database files.
        verbose (bool): Flag to enable verbose logging.
        reset_db (bool): Flag to indicate if the database should be reset.
        enable_cache (bool): Flag to enable caching.
        format_type (str): The format type of the response ('data', 'context', or 'api').
        reset_collection (bool): Flag to reset the collection.
        overwrite_file (bool): Flag to enable overwriting files.
        custom_prompt (str): Custom prompt for generating responses.
        prompt_override (bool): Flag to override default prompt.
        embedding (dict): Settings for embedding configuration.
        vector_store (dict): Settings for vector store configuration.
        llm_context (dict): Settings for LLM context configuration.
        llm_data (dict): Settings for LLM data configuration.
        remote_data_connections (dict): Dictionary of named remote data connections.
        data (dict): Additional data settings.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the Settings instance with default values and load settings from files or kwargs.

        Args:
            **kwargs: Additional keyword arguments for settings.
        """
        # Set default values
        self.path = os.path.abspath(os.getcwd())
        self.cache_dir = CACHE_DIR
        self.chart_dir = CHART_DIR
        self.log_dir = LOG_DIR
        self.db_path = DUCKDB_PATH
        self.vector_db_path = VECTOR_DIR

        # Verify and create directories if they don't exist
        self.create_directory(self.cache_dir)
        self.create_directory(self.chart_dir)
        self.create_directory(self.log_dir)
        self.create_directory(self.db_path)
        self.create_directory(self.vector_db_path)

        self.verbose = False
        self.reset_db = False
        self.enable_cache = False
        self.format_type = 'data'  # data, context or api
        self.reset_collection = False
        self.overwrite_file = False
        self.custom_prompt = ""
        self.prompt_override = False
        self.embedding = {
            'embedding_type': 'fastembed'
        }
        self.vector_store = {
            'store_type': 'chromadb',
            'persist_directory': self.vector_db_path,
            'db_name': 'datadashr',
            'api_key': None
        }

        self.llm_context = {
            'model_name': 'llama3',
            'api_key': None,
            'llm_type': 'ollama'
        }

        self.llm_data = {
            'model_name': 'codestral',
            'api_key': None,
            'llm_type': 'ollama'
        }
        self.data = {}

        self.remote_data_connections = {
            'mysql_default': {
                'dialect': os.getenv('DIALECT', 'mysql'),
                'driver': os.getenv('DRIVER', 'pymysql'),
                'host': os.getenv('HOST', 'localhost'),
                'port': int(os.getenv('PORT', 3306)),
                'database': os.getenv('DATABASE', 'mydb'),
                'username': os.getenv('USERNAME', 'root'),
                'password': os.getenv('PASSWORD', 'root')
            },
            'elasticsearch_default': {
                'host': os.getenv('ES_HOST', 'localhost'),
                'port': int(os.getenv('ES_PORT', 9200)),
                'username': os.getenv('ES_USERNAME', 'elastic'),
                'password': os.getenv('ES_PASSWORD', 'changeme')
            }
        }

        # Load settings from file if provided or found
        if settings_file := kwargs.get('settings_file') or (
                find_settings_file('datadashr_settings.json')
                or find_settings_file('datadashr_settings.yaml')
        ):
            self.load_from_file(settings_file)
        else:
            self.load_from_kwargs(kwargs)

        # Override default values with provided kwargs
        self.update_settings(kwargs)

    def create_directory(self, path: str) -> None:
        """
        Create a directory if it does not exist.

        Args:
            path (str): The path to the directory to be created.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def load_from_file(self, file_path: str) -> None:
        """
        Load settings from a JSON or YAML file.

        Args:
            file_path (str): The path to the settings file.
        """
        with open(file_path, 'r') as file:
            if file_path.endswith('.json'):
                settings = json.load(file)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                settings = yaml.safe_load(file)
            else:
                raise ValueError("Unsupported file type. Please use a JSON or YAML file.")
        self.load_from_kwargs(settings)

    def load_from_kwargs(self, kwargs: dict) -> None:
        """
        Load settings from keyword arguments.

        Args:
            kwargs (dict): The dictionary of keyword arguments.
        """
        root_path = kwargs.get('root_path', os.path.abspath(os.getcwd()))
        self.path = root_path
        self.verbose = kwargs.get('verbose', self.verbose)
        self.reset_db = kwargs.get('reset_db', self.reset_db)
        self.enable_cache = kwargs.get('enable_cache', self.enable_cache)
        self.format_type = kwargs.get('format_type', self.format_type)
        self.reset_collection = kwargs.get('reset_collection', self.reset_collection)
        self.overwrite_file = kwargs.get('overwrite_file', self.overwrite_file)
        self.custom_prompt = kwargs.get('custom_prompt', self.custom_prompt)
        self.prompt_override = kwargs.get('prompt_override', self.prompt_override)
        self.embedding = recursive_update(self.embedding, kwargs.get('embedding', {}))
        self.vector_store = recursive_update(self.vector_store, kwargs.get('vector_store', {}))
        self.llm_data = recursive_update(self.llm_data, kwargs.get('llm_data', {}))
        self.llm_context = recursive_update(self.llm_context, kwargs.get('llm_context', {}))
        self.remote_data_connections = recursive_update(self.remote_data_connections,
                                                        kwargs.get('remote_data_connections', {}))
        self.data = kwargs.get('data', self.data)

    def update_settings(self, kwargs: dict) -> None:
        """
        Update settings with new values from keyword arguments.

        Args:
            kwargs (dict): The dictionary of keyword arguments.
        """
        self.load_from_kwargs(kwargs)


