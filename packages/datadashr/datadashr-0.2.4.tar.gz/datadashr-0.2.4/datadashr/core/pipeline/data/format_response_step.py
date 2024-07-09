import json
import datetime
from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class FormatResponseStep(DataStep):
    """
    FormatResponseStep is a pipeline step that formats the results into a JSON response and adds it to the context.
    It extends the DataStep class.

    Methods:
        execute(self, context):
            Formats the results into a JSON response and adds it to the context.
    """

    def execute(self, context):
        """
        Format the results into a JSON response and add it to the context.

        Args:
            context: The context object containing the results.

        Returns:
            None
        """
        results = context.results

        # Custom encoder to handle datetime objects
        def datetime_encoder(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        context.add_property('formatted_response', json.dumps(results, indent=4, default=datetime_encoder))
        if context.verbose:
            logger.info(f"{self.name}: Formatted response {context.formatted_response}")
