from datadashr.core.pipeline.data_step import DataStep
from datadashr.core.utilities.cache import CacheManager
from datadashr.config import *


class SaveCacheStep(DataStep):
    """
    SaveCacheStep is a pipeline step that saves the current state to the cache. It extends the DataStep class.

    Methods:
        execute(self, context):
            Executes the save cache step and saves the current state to the cache if caching is enabled.

        _save_to_cache(self, context, data_connector, request):
            Saves the current state to the cache.
    """

    def execute(self, context):
        """
        Execute the save cache step.

        Args:
            context: The context object containing the request and cache settings.

        Returns:
            None
        """
        try:
            request = context.request
            data_connector = context.data_connector
            if context.enable_cache:
                self._save_to_cache(context, data_connector, request)
        except Exception as e:
            if context.verbose:
                logger.error(f"{self.name}: An error occurred during cache saving: {e}")
            return

    def _save_to_cache(self, context, data_connector, request):
        """
        Save the current state to the cache.

        Args:
            context: The context object containing the request and cache settings.
            data_connector: The data connector object.
            request: The request object.

        Returns:
            None
        """
        settings = context.settings
        cache_manager = CacheManager(
            db_folder=settings.cache_dir,
            delete_cache=settings.reset_db or False,
            verbose=context.verbose or False,
        )
        tables = data_connector.existing_tables()
        table_info = data_connector.table_info()
        llm_response = context.llm_response

        if not isinstance(llm_response, dict):
            if context.verbose:
                logger.error(f"{self.name}: llm_response is not in the correct format.")
            return

        cache_manager.set(
            query=request,
            tables=tables,
            fields=table_info,
            response=llm_response,
        )
        if context.verbose:
            logger.info(f"{self.name}: Cache saved for request")
