from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class ExtractQueriesStep(DataStep):
    """
    ExtractQueriesStep is a pipeline step that extracts queries from the LLM response and adds them to the context.
    It extends the DataStep class.

    Methods:
        execute(self, context):
            Extracts queries from the LLM response and adds them to the context.
    """

    def execute(self, context):
        """
        Extract queries from the LLM response and add them to the context.

        Args:
            context: The context object containing the LLM response.

        Returns:
            None
        """
        context.add_property('queries', context.llm_response)
        if context.verbose:
            logger.info(f"{self.name}: Extracted queries {context.queries}")
