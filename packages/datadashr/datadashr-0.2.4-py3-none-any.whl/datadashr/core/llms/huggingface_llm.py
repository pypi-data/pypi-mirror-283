from datadashr.core.llms.base_llm import BaseLLM
from datadashr.core.llms.check_llms import LLMChecker


class HuggingfaceLLM(BaseLLM):
    """
    HuggingfaceLLM is a concrete implementation of the BaseLLM class for the Huggingface model.
    It provides methods to check requirements, retrieve the model, and generate responses from a given prompt.

    Methods:
        default_model_name(self):
            Returns the default model name for the Huggingface LLM.

        check_requirements(self):
            Checks and ensures that all requirements for using the Huggingface LLM are met.

        get_model(self):
            Retrieves an instance of the Huggingface LLM model.

        chat(self, prompt):
            Generates a response based on a given prompt using the Huggingface LLM model.
    """

    @property
    def default_model_name(self):
        """
        Return the default model name for Huggingface LLM.

        Returns:
            str: The default model name.
        """
        return "bert-base-uncased"

    def check_requirements(self):
        """
        Checks and ensures that all requirements for using the Huggingface LLM are met.
        """
        self.api_key = LLMChecker.check_huggingface(self.model_name, self.api_key)

    def get_model(self):
        """
        Retrieve an instance of the Huggingface LLM model.

        Returns:
            HuggingFaceEndpoint: An instance of the Huggingface LLM model.
        """
        from langchain_huggingface import HuggingFaceEndpoint
        accepted_keys = ['model', 'api_key', 'temperature', 'max_tokens', 'top_p', 'frequency_penalty',
                         'presence_penalty']
        filtered_kwargs = self.filter_kwargs(accepted_keys)
        self.api_key = filtered_kwargs.pop('api_key', None)
        self.check_requirements()
        return HuggingFaceEndpoint(model=self.model_name, **filtered_kwargs)

    def chat(self, prompt):
        """
        Generate a response based on a given prompt using the Huggingface LLM model.

        Args:
            prompt (str or list): The prompt to generate a response for. Can be a string or a list of messages.

        Returns:
            Any: The generated response.
        """
        model = self.get_model()
        if isinstance(prompt, list):
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in prompt])
        else:
            prompt = prompt
        return model.invoke(prompt)
