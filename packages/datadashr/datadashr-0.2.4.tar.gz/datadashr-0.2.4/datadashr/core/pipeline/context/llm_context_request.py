from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.llms import LLM
from datadashr.config import *


class LLMContextRequestStep(DataStep):
    """
    LLMContextRequestStep is a pipeline step that sends a formatted prompt to a Large Language Model (LLM)
    and stores the response
    in the context. It extends the DataStep class.

    Methods:
        __init__(self, name="LLMContextRequest"):
            Initializes the LLMContextRequestStep with a default name.

        execute(self, context):
            Sends a formatted prompt to the LLM, retrieves the response, and adds it to the context.
            If an error occurs, it logs the error and sets the LLM response to an empty string.
    """

    def __init__(self, name="LLMContextRequest"):
        """
        Initialize the LLMContextRequestStep with a default name.

        Args:
            name (str, optional): The name of the step. Defaults to "LLMContextRequest".
        """
        super().__init__(name)

    def execute(self, context):
        """
        Send a formatted prompt to the LLM, retrieve the response, and add it to the context.

        Args:
            context: The context object containing the formatted prompt and LLM configuration.

        Raises:
            Exception: If an error occurs during the LLM request, it logs the error and sets the LLM response
            to an empty string.
        """
        try:
            llm_context = context.llm_context
            llm_instance = LLM(
                llm_type=llm_context.get('llm_type'),
                model_name=llm_context.get('model_name')
            )
            prompt = context.formatted_prompt
            response = llm_instance.chat(prompt)
            context.add_property('llm_response', response)
            logger.info(f"LLM response: {response}")
        except Exception as e:
            logger.error(f"Error in LLMContextRequestStep: {e}")
            context.add_property('llm_response', "")
