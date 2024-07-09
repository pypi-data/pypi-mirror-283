from datadashr.core.llms.base_llm import BaseLLM
from datadashr.core.llms.check_llms import LLMChecker


class OllamaLLM(BaseLLM):
    """
    OllamaLLM is a concrete implementation of the BaseLLM class for the Ollama model.
    It provides methods to check requirements, retrieve the model, and generate responses from a given prompt.

    Methods:
        default_model_name(self):
            Returns the default model name for the Ollama LLM.

        check_requirements(self):
            Checks and ensures that all requirements for using the Ollama LLM are met.

        get_model(self):
            Retrieves an instance of the Ollama LLM model.

        chat(self, prompt):
            Generates a response based on a given prompt using the Ollama LLM model.
    """

    @property
    def default_model_name(self):
        """
        Return the default model name for Ollama LLM.

        Returns:
            str: The default model name.
        """
        return "nomic-embed-text:latest"

    def check_requirements(self):
        """
        Checks and ensures that all requirements for using the Ollama LLM are met.
        """
        self.model_name = LLMChecker.check_ollama(self.model_name)

    def get_model(self):
        """
        Retrieve an instance of the Ollama LLM model.

        Returns:
            Ollama: An instance of the Ollama LLM model.
        """
        self.check_requirements()
        from langchain_community.llms import Ollama
        accepted_keys = ['model', 'base_url', 'temperature', 'top_k', 'top_p', 'timeout',
                         'repeat_penalty']
        filtered_kwargs = self.filter_kwargs(accepted_keys)
        return Ollama(model=self.model_name, **filtered_kwargs)

    def chat(self, prompt):
        """
        Generate a response based on a given prompt using the Ollama LLM model.

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
