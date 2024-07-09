import re
from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *
from typing import List, Tuple, Dict


class FormatResponseStep(DataStep):
    def execute(self, context):
        """
        Execute the response formatting step
        :param context: 
        :return: 
        """
        try:
            self._extracted_from_execute(context)
        except Exception as e:
            logger.error(f"{self.name}: Error formatting response: {e}")

    def _extracted_from_execute(self, context):
        blocks = re.findall(r"####\s*START\s*(.*?)####\s*END\s*", context, re.DOTALL)
        if not blocks:
            raise ValueError("The response does not contain valid blocks delimited by #### START and #### END.")

        queries = {'chart': [], 'table': []}
        for block in blocks:
            block_type_match = re.search(r"##\s*(Table|Chart)\s*:", block)
            if not block_type_match:
                continue
            block_type = block_type_match.group(1).strip().lower()
            query_match = re.search(r"```sql\s*(.*?)\s*```", block, re.DOTALL)
            if not query_match:
                continue
            query = query_match.group(1).strip()
            if not query.startswith("SELECT"):
                if "SELECT" not in query:
                    raise ValueError("The query does not start with 'SELECT' keyword.")
                else:
                    query = query[query.index("SELECT"):]
            queries[block_type].append(query)

        return queries

    def parse_results(self, query: str, results: List[Tuple]) -> List[Dict[str, str]]:
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

        return parsed_results
