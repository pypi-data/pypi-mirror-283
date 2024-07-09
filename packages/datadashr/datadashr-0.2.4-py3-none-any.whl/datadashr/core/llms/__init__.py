from datadashr.core.llms.openai_llm import OpenAILLM
from datadashr.core.llms.huggingface_llm import HuggingfaceLLM
from datadashr.core.llms.ollama_llm import OllamaLLM
from datadashr.core.llms.groq_llm import GroqLLM


class LLM:
    """
    LLM is a factory class that provides an interface for creating and managing various types of Large Language Models.
    It supports OpenAI, Huggingface, Ollama, and Groq LLMs.

    Attributes:
        LLM_CLASSES (dict): A dictionary mapping LLM type names to their corresponding classes.

    Methods:
        __new__(cls, llm_type, model_name=None):
            Creates a new instance of the specified LLM type.

        available_llms(cls):
            Returns a list of available LLM types.
    """

    LLM_CLASSES = {
        'openai': OpenAILLM,
        'huggingface': HuggingfaceLLM,
        'ollama': OllamaLLM,
        'groq': GroqLLM,
    }

    def __new__(cls, llm_type, model_name=None):
        """
        Create a new instance of the specified LLM type.

        Args:
            llm_type (str): The type of LLM to create (e.g., 'openai', 'huggingface', 'ollama', 'groq').
            model_name (str, optional): The name of the model to use.
            Defaults to the default model name of the LLM class.

        Returns:
            BaseLLM: An instance of the specified LLM class.

        Raises:
            ValueError: If the specified LLM type is not supported.
        """
        if llm_type not in cls.LLM_CLASSES:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
        llm_class = cls.LLM_CLASSES[llm_type]
        llm_instance = llm_class(model_name)
        llm_instance.get_model()  # Initialize the LLM model
        return llm_instance

    @classmethod
    def available_llms(cls):
        """
        Return a list of available LLM types.

        Returns:
            list: A list of available LLM types.
        """
        return list(cls.LLM_CLASSES.keys())


# Esempio di utilizzo
if __name__ == "__main__":
    available_llms = LLM.available_llms()
    print(f"Available LLMs: {available_llms}")

    # Utilizzo con modello specificato e chiave API
    """llm = LLM(llm_type='openai', model_name='davinci', api_key='your_api_key')
    response = llm.generate_text('Hello, world!')
    print(response)

    # Utilizzo con modello di default senza chiave API
    llm = LLM(llm_type='gpt')
    print(llm.model_info)
    print(llm.generate_text('Hello, world!'))

    llm = LLM(llm_type='huggingface', model_name='microsoft/Phi-3-mini-4k-instruct')
    print(llm.model_info)
    print(llm.generate_text('Hugging Face is'))"""

    llm = LLM(llm_type='ollama', model_name='llama3')
    print(llm.model_info)
    print(llm.generate_text('Ollama model'))
