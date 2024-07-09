import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import Keyword
from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class ValidateQueriesStep(DataStep):
    """
    ValidateQueriesStep is a pipeline step that validates and cleans SQL queries.
    It extends the DataStep class.

    Methods:
        execute(self, context):
            Validates and cleans the SQL queries, categorizing them as valid or invalid.

        _clean_query(self, query: str) -> str:
            Cleans the SQL query and resolves column ambiguities.

        extract_table_aliases(query: str) -> dict:
            Extracts table aliases from the SQL query.

        resolve_column_ambiguity(self, query: str, table_aliases: dict) -> str:
            Resolves column ambiguities in the SQL query.

        resolve_identifier(identifier: Identifier, table_aliases: dict):
            Resolves column ambiguities in a SQL identifier.
    """

    def execute(self, context):
        """
        Execute the query validation step.

        Args:
            context: The context object containing the SQL queries.

        Returns:
            None
        """
        queries = context.queries
        valid_queries = {}
        invalid_queries = {}

        for query_type, query_list in queries.items():
            for query in query_list:
                try:
                    if not query:
                        raise ValueError("Empty query")
                    if context.verbose:
                        logger.info(f"{self.name}: Validating query {query}")
                    cleaned_query = self._clean_query(query)
                    if context.verbose:
                        logger.info(f"{self.name}: Cleaned query {cleaned_query}")
                    valid_queries.setdefault(query_type, []).append(cleaned_query)
                except ValueError as e:
                    invalid_queries.setdefault(query_type, []).append(query)
                    logger.error(f"{self.name}: Invalid query {query}: {e}")

        context.add_property('invalid_queries', invalid_queries)
        context.add_property('valid_queries', valid_queries)
        if context.verbose:
            logger.info(f"{self.name}: Valid queries {valid_queries}")
            logger.info(f"{self.name}: Invalid queries {invalid_queries}")

    def _clean_query(self, query: str) -> str:
        """
        Clean the SQL query and resolve column ambiguities.

        Args:
            query (str): The SQL query to be cleaned.

        Returns:
            str: The cleaned SQL query.

        Raises:
            ValueError: If the query does not start with an accepted keyword.
        """
        query = query.strip()
        accepted_start_keywords = ["SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN"]
        if not any(query.startswith(keyword) for keyword in accepted_start_keywords):
            raise ValueError(f"Invalid query: {query}")
        table_aliases = self.extract_table_aliases(query)
        query = self.resolve_column_ambiguity(query, table_aliases)
        return query.replace("\n", " ").strip()

    @staticmethod
    def extract_table_aliases(query: str) -> dict:
        """
        Extract table aliases from the SQL query.

        Args:
            query (str): The SQL query.

        Returns:
            dict: A dictionary mapping table aliases to table names.
        """
        table_aliases = {}
        parsed = sqlparse.parse(query)[0]
        from_seen = False
        for token in parsed.tokens:
            if from_seen:
                if isinstance(token, Identifier):
                    alias = token.get_real_name() or token.get_name()
                    name = token.get_name()
                    if alias != name:  # Only add to table_aliases if alias is different
                        table_aliases[alias] = name
                elif isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        alias = identifier.get_real_name() or identifier.get_name()
                        name = identifier.get_name()
                        if alias != name:  # Only add to table_aliases if alias is different
                            table_aliases[alias] = name
                if token.ttype is Keyword and token.value.upper() in ('JOIN', 'ON'):
                    from_seen = False
            elif token.ttype is Keyword and token.value.upper() == 'FROM':
                from_seen = True
        return table_aliases

    def resolve_column_ambiguity(self, query: str, table_aliases: dict) -> str:
        """
        Resolve column ambiguities in the SQL query.

        Args:
            query (str): The SQL query.
            table_aliases (dict): A dictionary mapping table aliases to table names.

        Returns:
            str: The SQL query with resolved column ambiguities.
        """
        parsed = sqlparse.parse(query)[0]
        for token in parsed.tokens:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    self.resolve_identifier(identifier, table_aliases)
            elif isinstance(token, Identifier):
                self.resolve_identifier(token, table_aliases)
        return str(parsed)

    @staticmethod
    def resolve_identifier(identifier: Identifier, table_aliases: dict):
        """
        Resolve column ambiguities in a SQL identifier.

        Args:
            identifier (Identifier): The SQL identifier.
            table_aliases (dict): A dictionary mapping table aliases to table names.
        """
        if '.' not in str(identifier):
            col_name = str(identifier).strip('`')
            for alias, table in table_aliases.items():
                if col_name in table_aliases:
                    identifier.tokens = [sqlparse.sql.Token(None, f"{alias}.{col_name}")]
                else:
                    identifier.tokens = [sqlparse.sql.Token(None, col_name)]
