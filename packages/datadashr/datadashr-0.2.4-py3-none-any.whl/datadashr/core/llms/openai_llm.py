from datadashr.core.llms.base_llm import BaseLLM
from datadashr.core.llms.check_llms import LLMChecker


class OpenAILLM(BaseLLM):
    """
    OpenAILLM is a concrete implementation of the BaseLLM class for the OpenAI model.
    It provides methods to check requirements, retrieve the model, and generate responses from a given prompt.

    Methods:
        default_model_name(self):
            Returns the default model name for the OpenAI LLM.

        check_requirements(self):
            Checks and ensures that all requirements for using the OpenAI LLM are met.

        get_model(self):
            Retrieves an instance of the OpenAI LLM model.

        chat(self, prompt):
            Generates a response based on a given prompt using the OpenAI LLM model.
    """

    @property
    def default_model_name(self):
        """
        Return the default model name for OpenAI LLM.

        Returns:
            str: The default model name.
        """
        return "text-davinci-003"

    def check_requirements(self):
        """
        Checks and ensures that all requirements for using the OpenAI LLM are met.
        """
        self.api_key = LLMChecker.check_openai(self.model_name, self.api_key)

    def get_model(self):
        """
        Retrieve an instance of the OpenAI LLM model.

        Returns:
            OpenAI: An instance of the OpenAI LLM model.
        """
        accepted_keys = ['model', 'api_key', 'temperature', 'max_tokens', 'top_p', 'frequency_penalty',
                         'presence_penalty']
        filtered_kwargs = self.filter_kwargs(accepted_keys)
        self.api_key = filtered_kwargs.pop('api_key', None)
        self.check_requirements()
        from langchain_openai import OpenAI

        return OpenAI(model=self.model_name, **filtered_kwargs)

    def chat(self, prompt):
        """
        Generate a response based on a given prompt using the OpenAI LLM model.

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
