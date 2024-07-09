class DataStep:
    """
    DataStep is a base class representing a single step in a data processing pipeline. Each step must implement
    the execute method.

    Methods:
        __init__(self, name):
            Constructor for DataStep.

        execute(self, context):
            Execute the data step.

        __or__(self, other):
            Overloads the '|' operator to concatenate DataStep instances or DataStepGroup.
    """

    def __init__(self, name):
        """
        Constructor for DataStep.

        Args:
            name (str): Name of the step.
        """
        self.name = name

    def execute(self, context):
        """
        Execute the data step.

        Args:
            context: Context object containing necessary information.

        Returns:
            None
        """
        raise NotImplementedError("Each step must implement the execute method")

    def __or__(self, other):
        """
        Overloads the '|' operator to concatenate DataStep instances or DataStepGroup.

        Args:
            other: Another DataStep instance or DataStepGroup.

        Returns:
            DataStepGroup: A new DataStepGroup containing the concatenated steps.

        Raises:
            ValueError: If the type of 'other' is not supported.
        """
        if isinstance(other, DataStep):
            return DataStepGroup([self, other])
        elif isinstance(other, DataStepGroup):
            return DataStepGroup([self] + other.steps)
        else:
            raise ValueError("Unsupported type for concatenation with DataStep")


class DataStepGroup(DataStep):
    """
    DataStepGroup is a class representing a group of DataStep instances.
    It executes all steps in the group sequentially.

    Methods:
        __init__(self, steps):
            Constructor for DataStepGroup.

        execute(self, context):
            Execute all steps in the group.
    """

    def __init__(self, steps):
        """
        Constructor for DataStepGroup.

        Args:
            steps (list): List of DataStep instances.
        """
        self.steps = steps
        super().__init__("DataStepGroup")

    def execute(self, context):
        """
        Execute all steps in the group.

        Args:
            context: Context object containing necessary information.

        Returns:
            None
        """
        for step in self.steps:
            step.execute(context)
