# from Libs.Pipeline.Demo.key_in_dict_validator_proxy import KeyInDictValidatorHook
# from Pipeline import *
import os
import sys

######################################################################
# PATH                                                               #
######################################################################
ROOT_DIR = None
SAVING_DIR = "./Savings"

list_dirs = [SAVING_DIR]
######################################################################
# Sources                                                            #
######################################################################

source1 = {
    "class": "MockSource",
    "params":{
        "data":{
            "source1":"source1"
        },
        "pad":"dict"
    },
    "disabled":False,
    "forced":True,
    "source":None,
    "dest":None,
}

######################################################################
# Validator                                                          #
######################################################################

key_in_dict_validator_hook_source1 = {
    "class": "KeyInDictValidatorHook",
    "params":{
        "key":"source1"
        # "key":"source2"
    }
}
######################################################################
# Processors                                                         #
######################################################################

addItemToDictProcessor1 = {
    "class": "AddItemToDictProcessor",
    "params":{
        "src_bloc_dict":"id@source1",
        "key": "addItemToDictProcessor1",
        "val": 1000
    },
    "save":{
        "path":f"{SAVING_DIR}/addItemToDictProcessor1.pickle",
        "disable":False
    },
    "disabled":False,
    "forced":False,
    "validator":"id@key_in_dict_validator_hook_source1"
}

addItemToDictProcessor2 = {
    "class": "AddItemToDictProcessor",
    "params":{
        "src_bloc_dict":"id@addItemToDictProcessor1",
        "key": "addItemToDictProcessor2",
        "val": 3000
    },
    "disabled":False,
    "forced":False,
    "save":{
        "path":f"{SAVING_DIR}/addItemToDictProcessor2.pickle",
        "disable":False
    },
}
######################################################################
# Sinks                                                              #
######################################################################
printSink = {
    "class": "PrintSink",
    "params":{
        "src": "id@addItemToDictProcessor2"
    },
    "disabled":False,
    "forced":False,
    "source":None,
    "dest":None
}
