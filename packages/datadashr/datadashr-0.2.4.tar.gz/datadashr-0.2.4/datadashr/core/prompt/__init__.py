from datadashr.config import *
from jinja2 import Environment, FileSystemLoader
from loguru import logger


class PromptManager:
    """
    Class to generate prompts for the user to solve a problem.
    """

    def __init__(self, data_connector, custom_prompt: str = "", prompt_override: bool = False,
                 data_connector_type='duckdb', **kwargs):
        """
        Constructor for PromptManager.

        Args:
            data_connector: The data connector object.
            custom_prompt (str): Custom prompt text.
            prompt_override (bool): Flag to indicate if custom prompt should override the default prompt.
            data_connector_type (str): Type of data connector.
            kwargs: Additional keyword arguments.
        """
        self.data_connector = data_connector
        self.custom_prompt = custom_prompt
        self.prompt_override = prompt_override
        self.data_connector_type = data_connector_type
        templates_path = os.path.join(os.path.dirname(__file__), 'templates', data_connector_type)
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.verbose = kwargs.get('verbose', False)

    def _existing_tables(self):
        """
        Retrieve existing tables from the data connector.

        Returns:
            set: A set of existing table names.
        """
        existing_tables = {table[0] for table in self.data_connector.conn.execute("SHOW TABLES").fetchall()}
        existing_tables.discard('relation_structure')
        sources = self.data_connector.tables

        if all(source in existing_tables for source in sources):
            if self.verbose:
                logger.info(f"return sources: {sources}")
            return set(sources)
        else:
            if self.verbose:
                logger.info(f"return existing_tables: {existing_tables}")
            return existing_tables or {}

    def _table_info(self):
        """
        Retrieve table information from the data connector.

        Returns:
            dict: A dictionary containing table information.
        """
        table_info = {
            table: self.data_connector.conn.execute(
                f"PRAGMA table_info('{table}')"
            ).fetchdf()
            for table in self._existing_tables()
        }
        return table_info or {}

    def _relations(self):
        """
        Retrieve relations between tables from the data connector.

        Returns:
            dict: A dictionary containing relations between tables.
        """
        try:
            query = """
            SELECT source1, key1, source2, key2
            FROM relation_structure
            """
            relations_df = self.data_connector.conn.execute(query).fetchdf()
            relations = relations_df.to_dict(orient='records')
            if self.verbose:
                logger.info(f"Relations: {relations}")
            return relations or {}
        except Exception as e:
            logger.error(f"Error fetching relations: {e}")
            return {}

    def _describe_table(self):
        """
        Retrieve table descriptions from the data connector.

        Returns:
            dict: A dictionary containing table descriptions.
        """
        descriptions = self.data_connector.descriptions
        if not descriptions:
            logger.info("No descriptions available.")
        return descriptions or {}

    def build_prompt_for_role(self):
        """
        Build prompt for role.

        Returns:
            str: The generated prompt for the role.
        """
        try:
            template = self.env.get_template('role.txt')
            return template.render().strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for role: {e}")
            return ""

    def build_prompt(self, request):
        """
        Build prompt for DataFrame.

        Args:
            request: The request for which the prompt is to be built.

        Returns:
            str: The generated prompt.
        """
        try:
            return self._extracted_from_build_prompt(request)
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for DataFrame: {e}")
            return ""

    def _extracted_from_build_prompt(self, request):
        """
        Extracted method for building prompt.

        Args:
            request: The request for which the prompt is to be built.

        Returns:
            str: The generated prompt.
        """
        if self.prompt_override:
            return self.custom_prompt

        template = self.env.get_template('prompt.txt')
        descriptions = self._describe_table()
        table_info = self._table_info()
        relations = self._relations()
        if self.verbose:
            logger.info(f"Relations passed to template: {relations}")
        return template.render(
            descriptions=descriptions,
            table_info=table_info,
            relations=relations,
            question=request
        ).strip()

    def build_prompt_for_error_correction(self, error_message, generated_code):
        """
        Build prompt for error correction.

        Args:
            error_message: The error message to be included in the prompt.
            generated_code: The generated code to be included in the prompt.

        Returns:
            str: The generated prompt for error correction.
        """
        try:
            template = self.env.get_template('error_correction.txt')
            return template.render(
                error_message=error_message,
                generated_code=generated_code
            ).strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for error correction: {e}")
            return ""
