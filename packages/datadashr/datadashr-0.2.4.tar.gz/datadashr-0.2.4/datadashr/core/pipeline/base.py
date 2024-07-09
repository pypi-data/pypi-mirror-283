from datadashr.config import *
from datadashr.core.pipeline.data_step import DataStepGroup


class Pipeline:
    """
    Pipeline is a class that represents a sequence of steps to be executed in a specified order.
    It manages the execution
    of each step and maintains the context throughout the process.

    Methods:
        __init__(self, context):
            Initializes the pipeline with the given context.

        add_step(self, step):
            Adds a step to the pipeline.

        run(self):
            Runs the pipeline and executes each step in sequence.
    """

    def __init__(self, context):
        """
        Initialize the pipeline with the given context.

        Args:
            context: The context object for the pipeline.
        """
        self.steps = []
        self.context = context
        logger.info(f"Pipeline initialized with context: {self.context.__dict__}")

    def add_step(self, step):
        """
        Add a step to the pipeline.

        Args:
            step: The step to be added. Can be a single step or a DataStepGroup.

        Returns:
            None
        """
        if isinstance(step, DataStepGroup):
            self.steps.extend(step.steps)
        else:
            self.steps.append(step)

    def run(self):
        """
        Run the pipeline and execute each step in sequence.

        Returns:
            The final context after all steps have been executed, or None if an error occurs.
        """
        try:
            for step in self.steps:
                if self.context.verbose:
                    logger.info(f"Running step: {step.name}")
                step.execute(self.context)
                # Log the context after each step for debugging purposes
                if self.context.verbose:
                    logger.info(f"Context after {step.name}: {self.context.__dict__}")
                if self.context.skip_sandbox:
                    break
            return self.context
        except Exception as e:
            logger.error(f"Error running pipeline: {e}")
            return None
