import json
from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.utilities.cache import CacheManager
from datadashr.config import *


class CacheStep(DataStep):
    """
    CacheStep is a pipeline step that handles caching for requests. It retrieves cached results if available
    and updates the context accordingly. It extends the DataStep class.

    Methods:
        execute(self, context):
            Executes the cache step, retrieving cached results if available and updating the context.

        _retrieve_from_cache(self, context, data_connector, request):
            Retrieves the cached result if available and updates the context.

        _set_context_defaults(context):
            Sets default values in the context when there is no cache hit or an error occurs.
    """

    def execute(self, context):
        """
        Execute the cache step.

        Args:
            context: The context object containing the request and cache settings.

        Raises:
            Exception: If an error occurs during the cache step, it logs the error and sets default context values.
        """
        try:
            request = context.request
            data_connector = context.data_connector
            if context.enable_cache:
                self._retrieve_from_cache(context, data_connector, request)
        except Exception as e:
            if context.verbose:
                logger.error(f"{self.name}: An error occurred during cache step: {e}")
            self._set_context_defaults(context)

    def _retrieve_from_cache(self, context, data_connector, request):
        """
        Retrieve the cached result if available.

        Args:
            context: The context object containing the request and cache settings.
            data_connector: The data connector object.
            request: The request object.

        Raises:
            json.JSONDecodeError: If there is an error decoding the cached result, it logs the error
            and sets default context values.
        """
        settings = context.settings
        cache_manager = CacheManager(
            db_folder=settings.cache_dir,
            delete_cache=settings.reset_db or False,
            verbose=context.verbose or False,
        )
        tables = data_connector.existing_tables()
        table_info = data_connector.table_info()

        if cached_result := cache_manager.get(
                query=request, tables=tables, fields=table_info
        ):
            try:
                # Convert the cached result from JSON string to dictionary if it's a string
                if isinstance(cached_result, str):
                    cached_result = json.loads(cached_result)

                if not isinstance(cached_result, dict):
                    if context.verbose:
                        logger.error(
                            f"{self.name}: Cached result is not in the correct format. "
                            f"Cache format {type(cached_result)}")
                        logger.info(f"{self.name}: Cached result: {cached_result}")
                    self._set_context_defaults(context)
                    return

                context.add_property('cached_result', cached_result)
                context.add_property('llm_response', cached_result)
                context.add_property('skip_prompt_generation', True)
                if context.verbose:
                    logger.info(f"{self.name}: Cache hit for request")
            except json.JSONDecodeError as e:
                if context.verbose:
                    logger.error(f"{self.name}: Error decoding cached result: {e}")
                self._set_context_defaults(context)
                return
        else:
            self._set_context_defaults(context)
            if context.verbose:
                logger.info(f"{self.name}: No cache hit for request")

    @staticmethod
    def _set_context_defaults(context):
        """
        Set default values in the context when there is no cache hit or an error occurs.

        Args:
            context: The context object.
        """
        context.add_property('cached_result', None)
        context.add_property('llm_response', None)
        context.add_property('skip_prompt_generation', False)
