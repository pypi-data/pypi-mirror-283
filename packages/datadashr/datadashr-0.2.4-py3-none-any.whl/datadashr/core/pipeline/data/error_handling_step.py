from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.llms import LLM
from datadashr.config import *


class ErrorHandlingStep(DataStep):
    """
    ErrorHandlingStep is a pipeline step that handles errors related to invalid queries.
    It sends an error message using a Large Language Model (LLM) and updates the context accordingly.
    It extends the DataStep class.

    Methods:
        execute(self, context):
            Checks for invalid queries, sends an error message using the LLM, and updates the context.
    """

    def execute(self, context):
        """
        Check for invalid queries, send an error message using the LLM, and update the context.

        Args:
            context: The context object containing the invalid queries and LLM configuration.

        Returns:
            None
        """
        if invalid_queries := context.invalid_queries:
            error_message = f"Invalid queries found: {invalid_queries}"
            llm_data = context.llm_data

            llm_instance = LLM(
                llm_type=llm_data.get('llm_type'),
                model_name=llm_data.get('model_name')
            )
            llm_instance.send_error_message(error_message)
            context.add_property('skip_sandbox', True)
        if context.verbose:
            logger.info(f"{self.name}: Error message sent for invalid queries")
        return
