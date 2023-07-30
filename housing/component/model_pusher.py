# In model push we will save our model and deploy it in the production to use it some places .

# saved_models is the directory where i will load the model for the prediction . we will load our model from saved_model directory and we will use that model for the prediction .




from housing.logger import logging
from housing.exception import HousingException
from housing.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact 
from housing.entity.config_entity import ModelPusherConfig
import os, sys
import shutil


class ModelPusher:
    # It tequires two thing model_pusher_config and model_evalutaion_artifact .
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact
                 ):
        try:
            logging.info(f"{'>>' * 30}Model Pusher log started.{'<<' * 30} ")
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact

        except Exception as e:
            raise HousingException(e, sys) from e

    def export_model(self) -> ModelPusherArtifact:
        try:
            # The model that we have trained that location we will get in evaluated_model_file_path . Here we are talking about best model file path .
            evaluated_model_file_path = self.model_evaluation_artifact.evaluated_model_path
            # In export_dir we will get the name of folder or timestamp folder which is present in saved_models directory .
            export_dir = self.model_pusher_config.export_dir_path
            # The below mentioned code line will give us the model file name .
            model_file_name = os.path.basename(evaluated_model_file_path)
            
            # Here we can prepare complete file path .
            export_model_file_path = os.path.join(export_dir, model_file_name)
            logging.info(f"Exporting model file: [{export_model_file_path}]")
            # Next we will create the directory .
            os.makedirs(export_dir, exist_ok=True)

            # Shutil.copy will copy the trained model location inside the export_model_file_path . I am using shutll.copy means we are copying from one locale directory to other .
            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)
            #we can call a function to save model to Azure blob storage/ google cloud strorage / s3 bucket
            logging.info(
                f"Trained model: {evaluated_model_file_path} is copied in export dir:[{export_model_file_path}]")
            
            model_pusher_artifact = ModelPusherArtifact(is_model_pusher=True,
                                                        export_model_file_path=export_model_file_path
                                                        )
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            return model_pusher_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            raise HousingException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 20}Model Pusher log completed.{'<<' * 20} ")



# Now our machine learning training pipeline is completed .