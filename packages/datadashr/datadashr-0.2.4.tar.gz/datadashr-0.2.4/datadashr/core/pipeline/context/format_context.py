from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class FormatContextStep(DataStep):
    """
    FormatContextStep is a pipeline step that formats the retrieved context and the user request
    into a structured prompt for a question-answering task. It extends the DataStep class.

    Methods:
        __init__(self, name="FormatContext"):
            Initializes the FormatContextStep with a default name.

        execute(self, context):
            Formats the retrieved context and the user request into a structured prompt and adds it to the context.
            If an error occurs, it logs the error and sets the formatted prompt to an empty list.
    """

    def __init__(self, name="FormatContext"):
        """
        Initialize the FormatContextStep with a default name.

        Args:
            name (str, optional): The name of the step. Defaults to "FormatContext".
        """
        super().__init__(name)

    def execute(self, context):
        """
        Format the retrieved context and the user request into a structured prompt and add it to the context.

        Args:
            context: The context object containing the request and the retrieved context.

        Raises:
            Exception: If an error occurs during formatting, it logs the error and sets the formatted prompt
            to an empty list.
        """
        try:
            query = context.request
            context_text = context.retrieved_context
            context.add_property('formatted_prompt', [
                {"role": "user",
                 "content": f"You are an assistant for question-answering tasks. Use the following pieces of retrieved "
                            f"context to answer the question. If you don't know the answer, just say that you "
                            f"don't know. Use three sentences maximum and keep the answer concise. "
                            f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"},
            ])

            logger.info(f"Formatted prompt: {context.formatted_prompt}")
        except Exception as e:
            logger.error(f"Error in FormatContextStep: {e}")
            context.add_property('formatted_prompt', [])
