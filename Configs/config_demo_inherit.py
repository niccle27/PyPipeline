# from Libs.Pipeline.Demo.key_in_dict_validator_proxy import KeyInDictValidatorHook
# from Pipeline import *
import os
import sys
base=["./config_demo.py"]

######################################################################
# Sinks                                                              #
######################################################################
printSink2 = {
    "class": "PrintSink",
    "params":{
        "src": "id@addItemToDictProcessor2"
    },
    "disabled":False,
    "forced":False,
    "source":None,
    "dest":None
}
