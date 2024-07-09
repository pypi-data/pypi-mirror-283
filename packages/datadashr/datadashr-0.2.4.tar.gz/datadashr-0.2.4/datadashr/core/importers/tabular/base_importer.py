class BaseImporter:
    """
    BaseImporter is an abstract base class that defines the interface for data importers.
    It provides a common structure for importing data from various sources through a connector.

    Attributes:
        connector: The connector used for data import operations.

    Methods:
        import_data(self, source, table_name, filters, reset):
            Abstract method that must be implemented by subclasses to import data from a specified source.
    """

    def __init__(self, connector):
        """
        Initialize the BaseImporter instance with a connector.

        Args:
            connector: The connector used for data import operations.
        """
        self.connector = connector

    def import_data(self, source, table_name, filters, reset):
        """
        Abstract method that must be implemented by subclasses to import data from a specified source.

        Args:
            source: The data source to import from.
            table_name: The name of the table to import data into.
            filters: The filters to apply during data import.
            reset: A flag indicating whether to reset the table before importing data.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("import_data method must be implemented by subclasses")
