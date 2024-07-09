from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.prompt import PromptManager
from datadashr.config import *


class PromptGenerationStep(DataStep):
    """
    PromptGenerationStep is a pipeline step that generates prompts for the Large Language Model (LLM).
    It extends the DataStep class.

    Methods:
        execute(self, context):
            Generates prompts for the LLM and adds them to the context.
    """

    def execute(self, context):
        """
        Execute the prompt generation step.

        Args:
            context: The context object containing the request and prompt settings.

        Returns:
            None
        """
        try:
            if context.skip_prompt_generation:
                return

            prompt_override = bool(context.custom_prompt)
            prompt_manager = PromptManager(
                data_connector=context.data_connector,
                custom_prompt=context.custom_prompt if prompt_override else '',
                prompt_override=prompt_override,
                data_connector_type=context.data_connector_type,
            )
            request = context.request
            prompt_content = prompt_manager.build_prompt(request)

            if context.verbose:
                logger.info(f"Generated prompt content: {prompt_content}")

            messages = [
                {"role": "system", "content": prompt_manager.build_prompt_for_role()},
                {"role": "user", "content": prompt_content}
            ]

            if context.verbose:
                logger.info(f"Messages to be sent to LLM: {messages}")

            context.add_property('llm_messages', messages)
        except Exception as e:
            if context.verbose:
                logger.error(f"{self.name}: An error occurred during prompt generation: {e}")
            context.add_property('llm_messages', None)
            return
