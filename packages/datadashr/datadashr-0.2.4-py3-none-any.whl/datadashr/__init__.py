"""
Author: Fabio Cantone
Email: dev@datadashr.com
Date: 2024-07-06
Version: 0.2.4
License: Custom License (Non-Commercial Use)
Description: This script defines the DataDashr class, which handles data import, context creation, and execution of a
             pipeline based on user requests and response modes. The class integrates various modules from the
             DataDashr library to achieve these functionalities.

License Details:
    Copyright (c) 2024 Datadashr

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    1. The above copyright notice and this permission notice shall be included in all
       copies or substantial portions of the Software.

    2. The Software may not be used for commercial purposes without explicit
       permission from the original author, Datadashr.

    3. The original author, Datadashr, retains the right to use the Software for
       commercial purposes.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import random
from datadashr.core.utilities import Utilities
from datadashr.core.pipeline import Pipeline, CacheStep, PromptGenerationStep, LLMRequestStep, ErrorHandlingStep, \
    FormatResponseStep, SaveCacheStep, ExtractQueriesStep, ExecuteQueriesStep, ValidateQueriesStep, \
    FormatContextResponseStep, LLMContextRequestStep, FormatContextStep, RetrieveContextStep
from datadashr.core.importers import Connector
from jinja2 import Environment, FileSystemLoader
from datadashr.settings import Settings
from datadashr.context import Context
from datadashr.config import *


class DataDashr:
    """
    DataDashr is a class that handles data import, context creation, and executes
    a pipeline based on the provided request and response mode.

    Attributes:
        settings (Settings): Configuration settings for the instance.
        data_connector (Connector): Connector instance for data import.
        data_connector_type (str): Type of data connector.
        logger (LogManager): Logger for logging information and errors.
        ut (Utilities): Utilities instance for helper functions.
        env (Environment): Jinja2 environment for response templates.
    """

    def __init__(self, data, **kwargs):
        """
        Initialize the DataDashr instance with the provided data and optional settings.

        Args:
            data (dict): Dictionary containing the data sources and their mapping.
                Example:
                    {
                        'sources': [
                            {"source_name": "employees", "connection_string": sql_config, "source_type": "sql",
                             "description": "Contains employee details including their department."},
                            {"source_name": "salaries", "connection_string": sql_config, "source_type": "sql",
                             "description": "Contains salary information for employees."},
                            {"source_name": "departments", "data": departments_df, "source_type": "polars",
                                "description": "Contains information about departments and their managers."},
                        ],
                        'mapping': {
                            "employeeid": ['employees', 'salaries'],
                            "department": ['employees', 'departments']
                        }
                    }
            **kwargs: Additional keyword arguments for settings.
        """
        self.settings = Settings(**kwargs)
        self.data_connector = Connector()
        self.data_connector_type = self.data_connector.connector_type()
        self.logger = LogManager(LOG_DIR)
        self.ut = Utilities(self.settings.verbose)
        self.data_connector.import_data(data, reset=self.settings.reset_db, vector_store=self.settings.vector_store,
                                        embedding=self.settings.embedding)
        self.env = Environment(loader=FileSystemLoader(FANCY_RESPONSE_TEMPLATE))

    def chat(self, request, response_mode='data'):
        """
        Process a chat request through the pipeline and return the formatted response.

        Args:
            request (str): The user's request.
            response_mode (str): The mode of response ('data' or 'context').

        Returns:
            str or dict: The formatted response or an error message.
        """
        if self.settings.verbose:
            logger.info(f"Executing pipeline for request: {request}")

        # Load responses template
        template = self.env.get_template('fancy_response.txt')
        response_text = template.render(request=request)
        responses = response_text.splitlines()
        logger.info(random.choice(responses))

        # Initialize context
        c = Context(settings=self.settings)
        # Add properties to context
        c.add_property('data_connector', self.data_connector)
        c.add_property('request', request)
        c.add_property('response_mode', response_mode)
        c.add_property('data_connector_type', self.data_connector_type)

        logger.info(f"Context: {c.__dict__}")

        # Create and configure the pipeline
        step = Pipeline(context=c)

        if response_mode == 'data':
            step.add_step(
                CacheStep("Cache") |
                PromptGenerationStep("PromptGeneration") |
                LLMRequestStep("LLMRequest") |
                ExtractQueriesStep("ExtractQueries") |
                ValidateQueriesStep("ValidateQueries") |
                ErrorHandlingStep("ErrorHandling") |
                ExecuteQueriesStep("ExecuteQueries") |
                FormatResponseStep("FormatResponse") |
                SaveCacheStep("SaveCache")
            )

        elif response_mode == 'context':
            step.add_step(
                RetrieveContextStep("RetrieveContext") |
                FormatContextStep("FormatContext") |
                LLMContextRequestStep("LLMContextRequest") |
                FormatContextResponseStep("FormatContextResponse")
            )

        # Execute the pipeline
        step.run()
        if self.settings.verbose:
            logger.info(f"Final context: {c.__dict__}")

        # Retrieve and return the formatted response
        formatted_response = c.formatted_response
        if self.settings.verbose:
            logger.info(f"Formatted response: {formatted_response}")
        if formatted_response is not None:
            return formatted_response
        else:
            return {'error': 'No formatted response available'}
