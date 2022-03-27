from ...base_blocs import Source
from Registry.registry import REGISTRY

@REGISTRY.register()
class MockSource(Source):
    def __init__(self, data, pad=None):
        super().__init__(data=data)
        self.pad = pad
        self.data = data
    def fill(self):
            pass
    def getData(self):
        return self.data