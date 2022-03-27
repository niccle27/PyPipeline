from ..base_blocs import InputBloc
from Registry.registry import REGISTRY

@REGISTRY.register()
class MockInputBloc(InputBloc):
    def __init__(self, data, pad: str=None):
        super().__init__(pad=pad)
        self.pad = pad
        self.data = data

    def getData(self):
        return self.data 