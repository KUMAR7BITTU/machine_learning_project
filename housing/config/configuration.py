
from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig, TrainingPipelineConfig

class configuartion:
   
    def __init__(self) -> None:
        pass

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
        pass

