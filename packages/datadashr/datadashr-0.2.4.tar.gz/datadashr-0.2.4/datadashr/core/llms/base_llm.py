class BaseLLM:
    """
    BaseLLM is an abstract base class for Large Language Models (LLMs).
    It provides a common interface and structure for different LLM implementations.

    Attributes:
        model_name (str): The name of the LLM model.
        api_key (str): The API key for accessing the LLM model.
        kwargs (dict): Additional keyword arguments for the LLM model.
        llm_model (Any): The instance of the LLM model.

    Methods:
        default_model_name(self):
            Abstract property that should be implemented by subclasses to return the default model name.

        check_requirements(self):
            Abstract method that should be implemented by subclasses to check the requirements for the LLM model.

        get_model(self):
            Abstract method that should be implemented by subclasses to retrieve the LLM model.

        model_info(self):
            Property that returns a dictionary containing model information.

        filter_kwargs(self, accepted_keys):
            Filters and returns the keyword arguments that are accepted by the LLM model.

        chat(self, prompt):
            Abstract method that should be implemented by subclasses to generate a response based on a given prompt.
    """

    def __init__(self, model_name=None, api_key=None, **kwargs):
        """
        Initialize the BaseLLM instance with a model name, API key, and additional keyword arguments.

        Args:
            model_name (str, optional): The name of the LLM model. Defaults to the default model name if not provided.
            api_key (str, optional): The API key for accessing the LLM model.
            kwargs (dict): Additional keyword arguments for the LLM model.
        """
        self.model_name = model_name or self.default_model_name
        self.api_key = api_key
        self.kwargs = kwargs
        self.llm_model = None

    @property
    def default_model_name(self):
        """
        Abstract property that should be implemented by subclasses to return the default model name.

        Returns:
            str: The default model name.

        Raises:
            NotImplementedError: If the subclass does not implement this property.
        """
        raise NotImplementedError("Subclasses should implement this property.")

    def check_requirements(self):
        """
        Abstract method that should be implemented by subclasses to check the requirements for the LLM model.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_model(self):
        """
        Abstract method that should be implemented by subclasses to retrieve the LLM model.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def model_info(self):
        """
        Property that returns a dictionary containing model information.

        Returns:
            dict: A dictionary containing the model name and API key.
        """
        return {
            "model_name": self.model_name,
            "api_key": self.api_key
        }

    def filter_kwargs(self, accepted_keys):
        """
        Filters and returns the keyword arguments that are accepted by the LLM model.

        Args:
            accepted_keys (list): A list of accepted keyword argument keys.

        Returns:
            dict: A dictionary of filtered keyword arguments.
        """
        return {key: value for key, value in self.kwargs.items() if key in accepted_keys}

    def chat(self, prompt):
        """
        Abstract method that should be implemented by subclasses to generate a response based on a given prompt.

        Args:
            prompt (str): The prompt to generate a response for.

        Returns:
            Any: The generated response.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")
