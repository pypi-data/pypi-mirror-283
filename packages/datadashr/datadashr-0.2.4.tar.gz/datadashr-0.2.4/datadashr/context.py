"""
Author: Fabio Cantone
Email: dev@datadashr.com
Date: 2024-07-06
Version: 0.2.4
License: Custom License (Non-Commercial Use)
"""


class Context:
    """
    Context class manages the execution context for the DataDashr pipeline.
    It initializes with settings and allows for additional properties to be dynamically added.

    Attributes:
        settings (Settings): Configuration settings for the context.
        llm_context (dict): Settings for the LLM context.
        llm_data (dict): Settings for the LLM data.
        verbose (bool): Flag to enable verbose logging.
        enable_cache (bool): Flag to enable caching.
        format_type (str): The format type of the response ('data', 'context', or 'api').
        embedding (dict): Settings for embedding configuration.
        vector_store (dict): Settings for vector store configuration.
        custom_prompt (str): Custom prompt for generating responses.
        formatted_response (Optional[str]): The formatted response, initially None.
        skip_sandbox (bool): Flag to skip the sandbox step.
        skip_prompt_generation (bool): Flag to skip the prompt generation step.
    """

    def __init__(self, settings):
        """
        Initialize the Context instance with settings and default values.

        Args:
            settings (Settings): The settings instance to initialize the context with.
        """
        self.settings = settings
        self.llm_context = settings.llm_context
        self.llm_data = settings.llm_data
        self.verbose = settings.verbose
        self.enable_cache = settings.enable_cache
        self.format_type = settings.format_type
        self.embedding = settings.embedding
        self.vector_store = settings.vector_store
        self.custom_prompt = settings.custom_prompt
        self.formatted_response = None
        self.skip_sandbox = False
        self.skip_prompt_generation = False

    def add_property(self, name, value):
        """
        Dynamically add a property to the Context instance.

        Args:
            name (str): The name of the property to add.
            value (Any): The value of the property to add.
        """
        setattr(self, name, value)
