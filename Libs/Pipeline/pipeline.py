from copy import deepcopy
from Libs.Pipeline.Generics.loader_input_bloc import LoaderInputBloc
from Registry.registry import REGISTRY
from .base_blocs import Processor, Sink, Proxy, Source, InputBloc
from .Generics import *
from . import utils as ut
from . import wrappers as wrap
from pprint import pprint
from ..Py_loader import py_loader
import os

class PipelineConfig(object):
    def __init__(self, data):
        if isinstance(data, str):
            path_config = data
            data = py_loader.load_py_as_dict_with_base(path_config)
        elif isinstance(data, dict):
            pass
        else:
            raise RuntimeError(f"Type of data ({data.__class__}) is not in [str, dict]")
        self.config = data
        self._correct_config()
        
    def _correct_config(self):
        for instance_id, v in self.config.items():
            if not isinstance(v, dict):
                continue
            self._correct_config_instance(instance_id)
            
    def _correct_config_instance(self, id_instance):
        instance_dict = self.config[id_instance]
        if instance_dict.get("corrected"):
            return
        instance_disable = instance_dict.get("disabled", False)
        initial_disable = instance_disable
        instance_forced = instance_dict.get("forced", False)
        initial_forced = instance_forced
        instance_params = instance_dict.get("params", {})
        for k,v in instance_params.items():
            if isinstance(v, str) and "id@" in v:
                id_v = v[3:]
                self._correct_config_instance(id_v)
                instance_v = self.config[id_v]    
                instance_v_disable = instance_v.get("disabled", False)
                if instance_v_disable:
                    instance_disable=True
                instance_v_forced = instance_v.get("forced", False)
                if instance_v_forced:
                    instance_forced=True
        instance_dict["initial_disabled"]=initial_disable
        instance_dict["disabled"] = instance_disable
        instance_dict["initial_forced"]=initial_forced
        instance_dict["forced"] = instance_forced
        instance_dict["corrected"] = True
        
    def _set_saving_abs_path(self, abs_path_root_dir):
        config_dict_copy = deepcopy(self.config)
        for instance_id, v in config_dict_copy.items():
            if not isinstance(v, dict):
                continue
            saving_dict = v.get("save")
            if saving_dict:
                relative_path = saving_dict["path"]
                path_merge = os.path.join(abs_path_root_dir, relative_path)
                abs_path_merge = os.path.abspath(path_merge)
                saving_dict["path"] = abs_path_merge
        return config_dict_copy


class Pipeline(object):
    def __init__(self, root_dir, config_dict):
        self.dict_instances={}
        self.config_dict = config_dict
        self.root_dir = root_dir
        
    def create_directories(self):
        list_rel_path_directories = self.config_dict["list_dirs"]
        for rel_path in list_rel_path_directories:
            abs_path = os.path.abspath(os.path.join(self.root_dir, rel_path))
            os.makedirs(abs_path, exist_ok=True)
                
    def _load_params(self, m_id, params):
        loaded_params = deepcopy(params)
        for k, v in params.items():
            if isinstance(v, str) and v[:3]=="id@":
                instance_m_id = v[3:]           
                is_forced = self.config_dict[instance_m_id]["forced"]
                is_disabled = self.config_dict[instance_m_id]["disabled"]
                if instance_m_id not in self.dict_instances:
                    instance = self._load_instance(instance_m_id)
                    if not isinstance(instance, InputBloc):
                        # TODO test raise the error
                        raise RuntimeError(f"{instance.__class__} is not of type InputBloc")
                else:
                    instance = self.dict_instances[instance_m_id]
                loaded_params[k] = instance
                if is_forced:
                    self.config_dict[m_id]["forced"] = True
                if is_disabled:
                    self.config_dict[m_id]["disabled"] = True
                
        return loaded_params
                
    def _load_instance(self, m_id):
        v = self.config_dict[m_id]
        class_name = v["class"]
        params = v["params"]
        is_forced = self.config_dict[m_id].get("forced", False)
        save_dict = self.config_dict[m_id].get("save")
        instance=None
        loaded_dict=None
        if save_dict and not is_forced:
            path_saved = save_dict.get("path")
            if path_saved:
                loaded_dict = ut.load_pickle(path_saved)
                if loaded_dict:
                    instance = LoaderInputBloc(m_id, path_saved)
        if not instance:
            loaded_params = self._load_params(m_id, params)
            m_class = REGISTRY[class_name]
            instance = m_class(**loaded_params)
            if save_dict and isinstance(instance, InputBloc):
                saving_disabled = save_dict.get("disable", False)
                saving_path = save_dict.get("path", None)
                if not saving_disabled and saving_path and saving_path!="":
                    instance = wrap.wrapGetDataSaving(instance, m_id, saving_path)
                    
        validator_id = self.config_dict[m_id].get("validator")
        if validator_id:
            validator_id = validator_id[3:]
            if validator_id not in self.dict_instances:
                validator_instance = self._load_instance(validator_id)
                if not isinstance(instance, InputBloc):
                    raise RuntimeError(f"{instance.__class__} is not of type InputBloc")
            else:
                validator_instance = self.dict_instances[validator_id]
            instance = wrap.wrapGetDataValidation(instance, m_id, validator_instance)
        if True:
            instance = wrap.wrapPrintStep(instance, m_id)      
        return instance

    def setup(self):
        for m_id, v in self.config_dict.items():
            if not isinstance(v, dict):
                continue
            class_name = v["class"]
            params = v["params"]
            instance = self._load_instance(m_id)
            self.dict_instances[m_id] = instance

    def process(self):
        for m_id, v in self.dict_instances.items():
            bloc_disabled = self.config_dict[m_id].get("disabled", False)
            bloc_forced = self.config_dict[m_id].get("forced", False)
            bloc_initial_forced = self.config_dict[m_id].get("initial_forced", False)
            if bloc_disabled:
                #TODO use logging
                print(f"{m_id} is disabled")
                continue
            elif bloc_initial_forced:
                #TODO use logging
                print(f"{m_id} is forced")                
            if bloc_forced:
                if issubclass(v.__class__, Sink):
                    v.flush()
                elif issubclass(v.__class__, Source):
                    v.fill()
                elif issubclass(v.__class__, Processor):
                    v.process()
                else:
                    pass
            if issubclass(v.__class__, Sink) :
                if not v.isFlushed:
                    v.flush()
                    
    def get_dependency_tree(self, key):
        self.dict_instances={}
        instance_config = self.config_dict[key]
        dict_dependency_tree = {}
        if isinstance(instance_config, dict):
            instance_params = instance_config.get("params", {})
            for k, v in instance_params.items():
                if isinstance(v, str) and "id@" in v:
                    id_param=v[3:]
                    child_dict_dependency_tree=self.get_dependency_tree(id_param)
                    class_name = self.config_dict[key]["class"]
                    tmp_dict={"class": class_name, "dependencies": child_dict_dependency_tree}
                    dict_dependency_tree[id_param] = tmp_dict
        return dict_dependency_tree
    
    def print_dependency(self, key):
        pprint(self.get_dependency_tree(key))
