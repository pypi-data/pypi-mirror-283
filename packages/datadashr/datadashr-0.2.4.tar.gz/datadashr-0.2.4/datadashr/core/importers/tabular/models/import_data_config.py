from pydantic import BaseModel
from typing import List, Dict
from .source_config import SourceConfig
from .source_mapping import SourceMapping


class ImportDataConfig(BaseModel):
    """
    ImportDataConfig is a Pydantic model that defines the configuration for importing data from various sources.

    Attributes:
        sources (List[SourceConfig]): A list of source configurations for the data import.
        mapping (Dict[str, List[SourceMapping]]): A dictionary mapping source fields to target fields.
        Defaults to an empty dictionary.
    """

    sources: List[SourceConfig]
    mapping: Dict[str, List[SourceMapping]] = {}

    class Config:
        """
        Pydantic model configuration to allow arbitrary types and forbid extra attributes during model initialization.
        """
        arbitrary_types_allowed = True
        extra = 'forbid'
