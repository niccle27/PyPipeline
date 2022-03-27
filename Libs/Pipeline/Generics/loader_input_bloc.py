from ..base_blocs import InputBloc
from Registry.registry import REGISTRY
from .. import utils as ut

@REGISTRY.register()
class LoaderInputBloc(InputBloc):
    def __init__(self,instance_id, path, pad: str=None):
        super().__init__(pad=pad)
        self.pad = pad
        self.path = path
        self.instance_id = instance_id

    def load(self):
        data = ut.load_pickle(self.path)
        #TODO using logging
        print(f"{self.instance_id}: Data loaded from {self.path}")
        self.data = data

    def getData(self):
        if self.data is None:
            self.load()
        return self.data 
