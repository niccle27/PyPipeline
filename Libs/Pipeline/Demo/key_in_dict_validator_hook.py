from Registry.registry import REGISTRY
from ..base_blocs import Hook

@REGISTRY.register()
class KeyInDictValidatorHook(Hook):
    def __init__(self, key):
        super().__init__()
        self.key=key

    def execute(self, data):
        if self.key not in data:
            return False
        return True

        