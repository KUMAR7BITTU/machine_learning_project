
from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig, TrainingPipelineConfig
from housing.util.util import read_yaml_file
from housing.logger import logging

# To get all constant mentiond in __init__.py file in constant folder , we will write below mentioned code .

from housing.constant import *

# Here * means it will include all the constants included in __init__.py file in constant folder .

import sys,os 
from housing.exception import HousingException

class configuartion:
   
    def __init__(self,config_file_path:str = CONFIG_FILE_PATH,current_time_stamp:str = CURRENT_TIME_STAMP) -> None:
        self.config_info = read_yaml_file(file_path=config_file_path)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        pass

    # The return type for get_data_ingestion_config will be entity (DataIngestionConfig). So, we have to import configuration.py from housing.entity.config_entity . similarly , for other functions also .

    def get_data_validation_config(self) -> DataValidationConfig:
        pass

    # Here return type is DataValidationConfig entity . And similary for rest also .
    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR, training_pipeline_config[TRAINING_PIPELINE_NAME_KEY], training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])

            training_pipeline_config = TrainingPipelineConfig(artifact_dir = artifact_dir)
            logging.info(f"Training pipeline config: {training_pipeline_config}")
            return training_pipeline_config

        except Exception as e:
            raise HousingException(e,sys) from e 

