import sys
import os
sys.path.append(os.path.abspath("./Libs"))

from Libs.Pipeline.pipeline import Pipeline , PipelineConfig
from Libs.Pipeline.Demo import *
from pprint import pprint

ROOT_DIR = "/tmp/Test"
PATH_CONFIG = "./Configs/config_demo.py"

list_dir_name =  [e for e in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, e))]
list_dir_path = sorted([os.path.join(ROOT_DIR, e) for e in list_dir_name])

global_pipeline_config = PipelineConfig(PATH_CONFIG)

for pipeline_root_dir in list_dir_path:
    config_dict = global_pipeline_config._set_saving_abs_path(pipeline_root_dir)
    pprint(config_dict)
    pipeline=Pipeline(pipeline_root_dir, config_dict)
    pipeline.create_directories()
    pipeline.setup()
    pipeline.process()

