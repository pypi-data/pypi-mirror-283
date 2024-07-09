from datadashr.core.pipeline.data_step import DataStep
from typing import List, Dict, Tuple
from datadashr.config import *


class ExecuteQueriesStep(DataStep):
    """
    ExecuteQueriesStep is a pipeline step that executes valid queries using the data connector and parses the results.
    It extends the DataStep class.

    Methods:
        execute(self, context):
            Executes valid queries, parses the results, and updates the context with the results.

        parse_results(self, query: str, results: List[Tuple]) -> List[Dict[str, str]]:
            Parses the results of a query and returns them as a list of dictionaries.
    """

    def execute(self, context):
        """
        Execute valid queries, parse the results, and update the context with the results.

        Args:
            context: The context object containing the valid queries and the data connector.

        Returns:
            None
        """
        queries = context.valid_queries
        logger.info(f"Queries to be executed: {queries}")
        results = {'chart': [], 'table': []}

        for query_type, query_list in queries.items():
            for query in query_list:
                if context.verbose:
                    logger.info(f"Executing query: {query}")
                query_results = context.data_connector.execute_query(query)
                if context.verbose:
                    logger.info(f"Query results: {query_results}")
                parsed_results = self.parse_results(query, query_results)
                if context.verbose:
                    logger.info(f"Parsed results: {parsed_results}")
                results[query_type].extend(parsed_results)

        context.add_property('results', results)
        if context.verbose:
            logger.info(f"{self.name}: Query execution results {results}")

    @staticmethod
    def parse_results(query: str, results: List[Tuple]) -> List[Dict[str, str]]:
        """
        Parse the results of a query and return them as a list of dictionaries.

        Args:
            query (str): The query string that was executed.
            results (List[Tuple]): The results of the query execution.

        Returns:
            List[Dict[str, str]]: The parsed results as a list of dictionaries.
        """
        select_clause = query.split(" FROM ")[0]
        select_clause = select_clause.replace("SELECT", "").strip()
        columns = [col.strip() for col in select_clause.split(",")]

        column_names = []
        for col in columns:
            if " AS " in col:
                column_names.append(col.split(" AS ")[1].strip())
            else:
                column_name = col.split(".")[-1].strip()
                column_names.append(column_name)

        parsed_results = []
        for result in results:
            row = {column_names[i]: result[i] for i in range(len(column_names))}
            parsed_results.append(row)

        return parsed_results or []
