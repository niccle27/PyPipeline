import sys
import os
sys.path.append(os.path.abspath("./Libs"))

from Libs.Pipeline.pipeline import Pipeline , PipelineConfig
from Libs.Pipeline.Demo import *
from pprint import pprint

PATH_CONFIG = "/home/niccle27/Documents/Projects/Active/Registry_python/Configs/config_demo.py"
# PATH_CONFIG = "/home/niccle27/Documents/Projects/Active/Registry_python/Configs/config_demo_inherit.py"

PATH_ROOT_DIR = "/tmp/Test"

global_pipeline_config = PipelineConfig(PATH_CONFIG)
config_dict = global_pipeline_config._set_saving_abs_path(PATH_ROOT_DIR)
# pprint(config_dict)
# exit(0)
pipeline=Pipeline(PATH_ROOT_DIR, config_dict)
# pipeline.print_dependency("printSink")

pipeline.create_directories()
pipeline.setup()
pipeline.process()

