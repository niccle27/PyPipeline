class Registry:
    glob_module_registry = dict()

    @classmethod
    def register(cls, name: str=None, force=False):
        """ Class method to register Executor class to the internal registry.
        Args:
            name (str): The name of the executor.
        Returns:
            The Executor class itself.
        """

        def inner_wrapper(wrapped_class):
            class_name = wrapped_class.__name__
            if name is not None:
                key = name
            else:
                key = class_name
            if force or name not in cls.glob_module_registry:
                cls.glob_module_registry[key] = wrapped_class
            else:
                raise Exception(f"Key [{key}] is already stored in registry")
            return wrapped_class

        return inner_wrapper
    def __getitem__(self, key):
        return Registry.glob_module_registry[key]

REGISTRY = Registry()
