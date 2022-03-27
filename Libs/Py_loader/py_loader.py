from modulefinder import Module
import re
import sys
import os
import importlib.machinery
from copy import deepcopy

def load_py_as_dict(abs_path_module):
    basename_module = os.path.basename(abs_path_module)
    path_dir_module = os.path.dirname(abs_path_module)
    module_name = basename_module.split(".")[0]
    loader = importlib.machinery.SourceFileLoader(module_name, abs_path_module)
    config = loader.load_module()
    dict_imported = config.__dict__
    list_auto_module_keys = [k for k in dict_imported.keys() if len(re.findall("__.*__", k))>0]
    list_key_to_remove = [k for k,v in dict_imported.items() if v.__class__.__name__ not in ["int", "float", "ndarray", "list", "dict", "str"]]
    exclude_list = list_auto_module_keys + list_key_to_remove
    data ={k:v for k,v in dict_imported.items() if k not in exclude_list}
    return data


def load_py_as_dict_with_base(abs_path_module):
    path_dir_module = os.path.dirname(abs_path_module)
    data = load_py_as_dict(abs_path_module)
    base_dict={}
    if "base" in data:
        for path_module in data["base"]:
            if "./" in path_module:
                abs_path_module = os.path.join(path_dir_module, path_module)
            else:
                abs_path_module = path_module
            abs_path_module = os.path.abspath(abs_path_module)
            base_data = load_py_as_dict_with_base(abs_path_module)
            base_dict = {**base_dict, **base_data}
            
    final_dict = deepcopy({**base_dict, **data})
    if "base" in final_dict:
        del final_dict["base"]
    return final_dict