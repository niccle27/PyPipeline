from .exceptions import *

class InputBloc(object):
    @staticmethod
    def check_pad(instance, pad_expected):
        if instance.pad != pad_expected:
            raise PadError(instance=instance, pad_expected=pad_expected)
        
    def __init__(self, pad: str=None, **kwargs):
        super().__init__(**kwargs)
        self.pad = pad
        self.data = None
        
    def getData(self):
        raise NotImplementedError       

class Hook(object):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        
    def execute(self):
        raise NotImplementedError
    
    def __call__(self, **kwargs):
        return self.execute(**kwargs)

class Loadable(object):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.list_loadable=[]
        
    def load(self):
        for loadable in self.list_loadable:
            loadable.getData()

class Hookable(object):
    def __init__(self, dict_hooks={},  **kwargs):
        super().__init__()
        self.dict_hooks = dict_hooks

    def process_hook(self, key, **kwargs):
        if key in self.dict_hooks:
            for hook in self.dict_hooks[key]:
                if not isinstance(hook, Hook):
                    raise RuntimeError(f"{hook.__class__} is not of type Hook")
                hook.execute(**kwargs)

class Source(InputBloc, Hookable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fill(self):
        raise NotImplementedError

    def getData(self):
        if self.data is None:
            self.fill()
        return self.data


class Sink(Hookable, Loadable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isFlushed=False
    def action(self):
        raise NotImplementedError
    def flush(self):
        self.load()
        self.action()
        self.isFlushed=True
            
class Processor(InputBloc, Hookable, Loadable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getData(self):
        self.load()
        if self.data is None:
            self.process()
        return self.data

    def process(self):
        raise NotImplementedError

class Proxy(object):
    def __call__(self, **kwargs):
        return self.through(**kwargs)

    def through(self, **kwargs):
        raise NotImplementedError
