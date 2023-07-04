# In every project , there is requirement to define hardcoded variable like where this config.yaml is located .

import os

ROOT_DIR = os.getcwd() # To get current working directory .

from datetime import datetime 

# wherever we will run python app.py file that particular directory location we will get 

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

# within root directory we will have config folder within which we will have config.yaml file .

# we are writing this kind of codes because i want this to run on type of system and it should not show error like path is supported .

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

# Training pipeline related variable 
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

# All constant will be managed in this file . 