from Registry.registry import REGISTRY
from ..base_blocs import Processor, InputBloc

@REGISTRY.register()
class AddItemToDictProcessor(Processor):
    def __init__(self, src_bloc_dict:InputBloc, key, val):
        super().__init__()
        InputBloc.check_pad(src_bloc_dict, "dict")  
        self.pad = "dict"
        self.key = key
        self.val = val
        self.src_bloc_dict = src_bloc_dict
        self.list_loadable=[self.src_bloc_dict]
    def process(self):
        data={}
        data_src_bloc_dict = self.src_bloc_dict.getData()
        if not isinstance(data_src_bloc_dict, dict):
            raise RuntimeError(f"{data_src_bloc_dict.__class__} is not of type dict")
        data = {**data_src_bloc_dict}
        data[self.key]=self.val
        self.data = data
        