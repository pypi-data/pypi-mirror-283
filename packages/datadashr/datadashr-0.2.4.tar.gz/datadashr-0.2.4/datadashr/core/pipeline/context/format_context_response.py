from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class FormatContextResponseStep(DataStep):
    """
    FormatContextResponseStep is a pipeline step that formats the response from the LLM (Large Language Model) and adds it
    to the context. It extends the DataStep class.

    Methods:
        __init__(self, name="FormatContextResponse"):
            Initializes the FormatContextResponseStep with a default name.

        execute(self, context):
            Formats the response from the LLM and adds it to the context.
            If an error occurs, it logs the error and sets the formatted response to an error message.
    """

    def __init__(self, name="FormatContextResponse"):
        """
        Initialize the FormatContextResponseStep with a default name.

        Args:
            name (str, optional): The name of the step. Defaults to "FormatContextResponse".
        """
        super().__init__(name)

    def execute(self, context):
        """
        Format the response from the LLM and add it to the context.

        Args:
            context: The context object containing the response from the LLM.

        Raises:
            Exception: If an error occurs during formatting, it logs the error and sets the formatted response
            to an error message.
        """
        try:
            llm_response = context.llm_response
            if isinstance(llm_response, str):
                context.formatted_response = llm_response
            elif isinstance(llm_response, list) and len(llm_response) > 0:
                context.formatted_response = llm_response[0].get('content', '')
            else:
                context.add_property('formatted_response', 'No response from LLM.')
            logger.info(f"Formatted response: {context.formatted_response}")
        except Exception as e:
            logger.error(f"Error in FormatContextResponseStep: {e}")
            context.formatted_response = 'Error formatting response.'
