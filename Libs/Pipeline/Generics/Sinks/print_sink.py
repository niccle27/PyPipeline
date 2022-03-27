from Registry.registry import REGISTRY
from ...base_blocs import Sink

@REGISTRY.register()
class PrintSink(Sink):
    def __init__(self, src):
        super().__init__()
        self.src = src
        self.list_loadable=[self.src ]
    def action(self):
        data_to_display = self.src.getData()
        print(data_to_display)
