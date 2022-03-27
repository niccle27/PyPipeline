from .base_blocs import *
from .Generics import LoaderInputBloc
from .exceptions import ValidationError
from . import utils as ut
def wrapGetDataSaving(instance, instance_id, path):
    if not isinstance(instance, InputBloc):
        raise RuntimeError(f"{instance.__class__} is not of type InputBloc")
    InstanceClass = instance.__class__
    class WrapClass(InstanceClass):
        def __init__(self, instance):
            self.__dict__ = instance.__dict__
            self.is_data_saved=None
        def getData(self):
            data = super().getData()
            if data and self.is_data_saved is None:
                ut.write_pickle(data, path)
                # TODO use logging
                print(f"Results of {instance_id} saved at {path}")
                self.is_data_saved = True
            return data
    wrapped_instance = WrapClass(instance)
    return wrapped_instance

def wrapGetDataValidation(instance, instance_id, validator_hook):
    if not isinstance(instance, InputBloc):
        raise RuntimeError(f"{instance.__class__} is not of type InputBloc")
    InstanceClass = instance.__class__
    class WrapClass(InstanceClass):
        def __init__(self, instance):
            self.__dict__ = instance.__dict__
            self.is_data_valid=None
        def getData(self):
            data = super().getData()
            if self.is_data_valid is None:
                self.is_data_valid = validator_hook(data=data)
            if not self.is_data_valid:
                raise ValidationError(f"Data from {instance_id} is not valid")
            return data
    wrapped_instance = WrapClass(instance)
    return wrapped_instance

def wrapPrintStep(instance, instance_id: str):
    InstanceClass = instance.__class__
    if isinstance(instance, Source):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def fill(self):
                print(f"Start filling {instance_id}")
                super().fill()
                print(f"Stop filling {instance_id}")

    elif isinstance(instance, Processor):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def process(self):
                print(f"Start processing {instance_id}")
                super().process()
                print(f"Stop processing {instance_id}")

    elif isinstance(instance, Sink):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def action(self):
                print(f"Start flushing {instance_id}")
                super().action()
                print(f"Stop flushing {instance_id}")

    elif isinstance(instance, Proxy):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def through(self):
                print(f"Start proxy through {instance_id}")
                super().through()
                print(f"Stop proxy through {instance_id}")

    elif isinstance(instance, Hook):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def execute(self, **kwargs):
                print(f"Start hook {instance_id}")
                ret = super().execute(**kwargs)
                print(f"Stop hook {instance_id}")
                return ret
                
    elif isinstance(instance, LoaderInputBloc):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def load(self):
                print(f"Start loading {instance_id}")
                super().load()
                print(f"Stop loading {instance_id}")
    else:
        raise RuntimeError(f"{instance.__class__} is not of types [Source|Processor|Sink|Proxy|Hook]")
    
    wrapped_instance = WrapClass(instance)
    return wrapped_instance

def wrapPrintStep(instance, instance_id: str):
    InstanceClass = instance.__class__
    if isinstance(instance, Source):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def fill(self):
                print(f"Start filling {instance_id}")
                super().fill()
                print(f"Stop filling {instance_id}")

    elif isinstance(instance, Processor):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def process(self):
                print(f"Start processing {instance_id}")
                super().process()
                print(f"Stop processing {instance_id}")

    elif isinstance(instance, Sink):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def action(self):
                print(f"Start flushing {instance_id}")
                super().action()
                print(f"Stop flushing {instance_id}")

    elif isinstance(instance, Proxy):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def through(self):
                print(f"Start proxy through {instance_id}")
                super().through()
                print(f"Stop proxy through {instance_id}")

    elif isinstance(instance, Hook):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def execute(self, **kwargs):
                print(f"Start hook {instance_id}")
                ret = super().execute(**kwargs)
                print(f"Stop hook {instance_id}")
                return ret
                
    elif isinstance(instance, LoaderInputBloc):
        class WrapClass(InstanceClass):
            def __init__(self, instance):
                self.__dict__ = instance.__dict__
            def load(self):
                print(f"Start loading {instance_id}")
                super().load()
                print(f"Stop loading {instance_id}")
    else:
        raise RuntimeError(f"{instance.__class__} is not of types [Source|Processor|Sink|Proxy|Hook]")
    
    wrapped_instance = WrapClass(instance)
    return wrapped_instance