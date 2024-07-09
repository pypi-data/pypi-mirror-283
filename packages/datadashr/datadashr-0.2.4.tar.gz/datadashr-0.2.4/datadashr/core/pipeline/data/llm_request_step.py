from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.llms import LLM
from datadashr.config import *
from typing import List, Dict
import re


class LLMRequestStep(DataStep):
    """
    LLMRequestStep is a pipeline step that sends a request to a Large Language Model (LLM), receives the response, and
    extracts queries from the response. It extends the DataStep class.

    Methods:
        execute(self, context):
            Sends a request to the LLM, receives the response, and extracts queries from the response.

        extract_queries(response: str) -> Dict[str, List[str]]:
            Extracts SQL queries from the LLM response and categorizes them as 'chart' or 'table' queries.
    """

    def execute(self, context):
        """
        Execute the LLM request step.

        Args:
            context: The context object containing the LLM data and messages.

        Returns:
            None
        """
        try:
            if context.skip_prompt_generation:
                return
            llm_data = context.llm_data

            llm_instance = LLM(
                llm_type=llm_data.get('llm_type'),
                model_name=llm_data.get('model_name')
            )
            messages = context.llm_messages

            if context.verbose:
                logger.info(f"{self.name}: Sending the following messages to the LLM: {messages}")

            try:
                response = llm_instance.chat(messages)
            except Exception as e:
                if context.verbose:
                    logger.error(f"{self.name}: An error occurred during LLM request: {e}")
                context.add_property('llm_response', None)
                return

            if context.verbose:
                logger.info(f"{self.name}: Received the following response from the LLM: {response}")

            if not response:
                if context.verbose:
                    logger.error(f"{self.name}: LLM request returned no valid response")
                context.add_property('llm_response', None)
            else:
                context.add_property('llm_response', self.extract_queries(response))
                if context.verbose:
                    logger.info(f"{self.name}: LLM request completed")
        except Exception as e:
            if context.verbose:
                logger.error(f"{self.name}: An error occurred during LLM request: {e}")
            context.add_property('llm_response', None)
            return

    @staticmethod
    def extract_queries(response: str) -> Dict[str, List[str]]:
        """
        Extract SQL queries from the LLM response and categorize them as 'chart' or 'table' queries.

        Args:
            response (str): The response from the LLM.

        Returns:
            Dict[str, List[str]]: A dictionary containing categorized SQL queries.

        Raises:
            ValueError: If the response does not contain valid blocks delimited by #### START and #### END
            or if queries do not start with 'SELECT'.
        """
        blocks = re.findall(r"####\s*START\s*(.*?)####\s*END\s*", response, re.DOTALL)
        if not blocks:
            raise ValueError("The response does not contain valid blocks delimited by #### START and #### END.")

        queries = {'chart': [], 'table': []}
        for block in blocks:
            block_type_match = re.search(r"##\s*(Table|Chart)\s*:", block)
            if not block_type_match:
                continue
            block_type = block_type_match[1].strip().lower()
            query_match = re.search(r"```sql\s*(.*?)\s*```", block, re.DOTALL)
            if not query_match:
                continue
            query = query_match[1].strip()
            if not query.startswith("SELECT"):
                if "SELECT" not in query:
                    raise ValueError("The query does not start with 'SELECT' keyword.")
                else:
                    query = query[query.index("SELECT"):]
            queries[block_type].append(query)

        return queries
