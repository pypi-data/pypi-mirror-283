import pandas as pd
import polars as pl
from pydantic import BaseModel, field_validator
from typing import Union, Dict, Any
from .config import SQLConfig


class SourceConfig(BaseModel):
    """
    SourceConfig is a Pydantic model that defines the configuration for a data source.

    Attributes:
        source_name (str): The name of the data source.
        source_type (str): The type of the data source (e.g., 'pandas', 'polars', 'csv', 'sql', 'elasticsearch',
        'parquet').
        description (str): A description of the data source. Defaults to "No description provided".
        delete_table (bool): Whether to delete the table before importing new data. Defaults to False.
        connection_string (Union[SQLConfig, None]): The SQL connection configuration. Defaults to None.
        data (Union[pd.DataFrame, pl.DataFrame, None]): The data to be imported. Defaults to None.
        file_path (Union[str, None]): The file path to the data source. Defaults to None.
        host (Union[str, None]): The host of the data source. Defaults to None.
        username (Union[str, None]): The username for the data source. Defaults to None.
        password (Union[str, None]): The password for the data source. Defaults to None.
        index (Union[str, None]): The index for the data source. Defaults to None.
        query (Union[str, None]): The query to be executed on the data source. Defaults to None.
        filter (Dict[str, Any]): A dictionary of filters to apply to the data source. Defaults to an empty dictionary.
        save_to_vector (bool): Whether to save the data to a vector store. Defaults to False.
    """

    source_name: str
    source_type: str
    description: str = "No description provided"
    delete_table: bool = False
    connection_string: Union[SQLConfig, None] = None
    data: Union[pd.DataFrame, pl.DataFrame, None] = None
    file_path: Union[str, None] = None
    host: Union[str, None] = None
    username: Union[str, None] = None
    password: Union[str, None] = None
    index: Union[str, None] = None
    query: Union[str, None] = None
    filter: Dict[str, Any] = {}
    save_to_vector: bool = False

    class Config:
        """
        Pydantic model configuration to allow arbitrary types and forbid extra attributes during model initialization.
        """
        arbitrary_types_allowed = True
        extra = 'forbid'  # Updated to use literal value as recommended

    @field_validator('source_type')
    def check_source_type(cls, value):
        """
        Validate the source type to ensure it is supported.

        Args:
            value (str): The source type to validate.

        Returns:
            str: The validated source type.

        Raises:
            ValueError: If the source type is not supported.
        """
        if value not in ['pandas', 'polars', 'csv', 'sql', 'elasticsearch', 'parquet']:
            raise ValueError(f"Unsupported source type: {value}")
        return value
