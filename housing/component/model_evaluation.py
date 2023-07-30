# If the trained model is not better the model which is in production , then our pipeline will not run futher . It will stop there . And if our trained model is better than the model which is in production then we will push that model into the production .

# I need some database or file to store my best model location . Inside model_evaluation.yaml file we will store the location(path) our best model . Here we are not using any databases to store location of our best model . We can load model from the model_evaluation.yaml file . The best model is the model which is in the production . And from the training model artifact we can get the new model . 

# from trained_model_file_path we can get the location of our trained model.from the model_trainer we can get the trained_model_file_path . Apart from that from the evaluation report i can get the best model .


# We have to compare LinearRegression and RandomForestRegression model which will be good , that model will be compared with the best model which is already available in the production .

# So, we need two location, First is location of our trained model and second is location our best model which is available in the production .


from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from housing.constant import *
import numpy as np
import os
import sys
from housing.util.util import write_yaml_file, read_yaml_file, load_object,load_data
from housing.entity.model_factory import evaluate_regression_model




class ModelEvaluation:
    
    # from data_ingestion_artifact we need training and testing dataset . from  model_trainer_artifact we can get the location of our trained model which we have trained and saved it there . From data_validation_artifact we need schema file . It basically give us the structure of our file .
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            logging.info(f"{'>>' * 30}Model Evaluation log started.{'<<' * 30} ")
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e
    
    # This function will give us best model .
    def get_best_model(self):
        try:
            model = None
            # We will get the path of best model location .
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path
            
            # If that best model location file is not available then we will return None . So, we are creating a empty file then we are returning None . It it check if file is not available then it will create an empty file then return None .
            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path,
                                )
                return model
            
            # If we have our best model in production then if statement will be ignored and we will read the model_evaluation_file_path content . It will give us dictionary .
            model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)
            
            # If model_eval_file_content will not contain anything then we will create empty dictionary and it contain something then we will just read it .
            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content
            
            # Next we are checking do we have best model key . If base model key is not available then we will simply return None . Right now our model is None .
            if BEST_MODEL_KEY not in model_eval_file_content:
                return model
            
            # So, if our file (best model file) is not available then we will return None . And also , if also content is not available in best-model file then also we will return None .

            # And if our best-model is available (which means the above two cases not present ) then we will read the MODEL_PATH_KEY .

            # And then we will load the model and if this line will be called then we will get our model .
            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            raise HousingException(e, sys) from e
    

    # In this function we have to do the comparision and if our train model is better than our best model in production then we should update the content in model_evaluation.yaml flle . It means we have to change the best model location . 
    # If our trained model will be better than the best moel which is in production then we will call update_evaluation_report function .
    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            # Then we need to know where is our model evaluation file .
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path

            # Then we will read the entire content of the file .
            model_eval_content = read_yaml_file(file_path=eval_file_path)

            # If we got None from model_eval_content as there we will no content in best-model file then we will initialize empty dictionay . If this is not the case then we will get the updated content .
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                # From below line of code we will get previous best model location .
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"Previous eval result: {model_eval_content}")
            
            # Here in below mentioned code we will create new best model path or evaluated model path .
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path,
                }
            }
            
            # if previous_best_model is not None then model_history will contain location of best model location in production and with timestamp .
            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                # if HISTORY_KEY is not present in model_eval_content then we will create a history section underwhich with timestamp  location of previous base model will be present .
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    # If HISTORY_KEY is present then we have to just update that history key .
                    model_eval_content[HISTORY_KEY].update(model_history)
            # In below mentioned line of code model_eval_content will be updated from None .
            model_eval_content.update(eval_result)
            logging.info(f"Updated eval result:{model_eval_content}")
            # Next we will write the new details in yaml file .
            write_yaml_file(file_path=eval_file_path, data=model_eval_content)

        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            # We need trained_model_file_path 
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            # we can get trained_model_object
            trained_model_object = load_object(file_path=trained_model_file_path)
            
            # we can get train_file_path and test_file_path from data_ingestion_artifact for comparision .
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path
            
            # By below mentioned code we can get train dataframe and test dataframe . We have not applied any feature engineering here because we are reading it form data ingestion phase . We have just splited training and test dataset .
            train_dataframe = load_data(file_path=train_file_path,
                                                           schema_file_path=schema_file_path,
                                                           )
            
            # From schema content we can get target column . We have to split input feature and target feature .
            test_dataframe = load_data(file_path=test_file_path,
                                                          schema_file_path=schema_file_path,
                                                          )
            
            schema_content = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema_content[TARGET_COLUMN_KEY]

            # target_column
            # Here we will convert target column into numpy array .
            logging.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array.")
            # from above code we will get our target feature .


            # dropping target column from the dataframe
            # As we have already extracted the target column , so we are droping this column .
            logging.info(f"Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            test_dataframe.drop(target_column_name, axis=1, inplace=True)
            logging.info(f"Dropping target column from the dataframe completed.")
            # from above code we will get input features .

            model = self.get_best_model()
            # We will get None if there will be no best model in the production . If there will be best model in the production then we will get that model .
            
            # If there is no model then we can directly save our trained model and update it in the production .
            if model is None:
                logging.info("Not found any existing model. Hence accepting trained model")
                # We are just creating model_evaluation_artifact
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                # Here , we are updating model_evaluation_artifact .
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")
                # Then model_evaluation-artifact will be return and rest part which is below it will not be executed .
                return model_evaluation_artifact
            
            # Here we will prepare the list of the best model and the trained model . So, trained model is new one and best model is existing one .
            model_list = [model, trained_model_object]
            # Here we will also store the index number .

            
            # In evaluate_regression_model we will pass the model_list which will contain the best model and trained model and also other parameters so that it can give us the best model between the best model which is available in production and trained model .Actually here we will do the comparision between the two model .
            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                               X_train=train_dataframe,
                                                               y_train=train_target_arr,
                                                               X_test=test_dataframe,
                                                               y_test=test_target_arr,
                                                               base_accuracy=self.model_trainer_artifact.model_accuracy,
                                                               )
            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")
            
            # If metric_info_artifact gives us None value then it means None of the model is better from each other or satisfy best acuraccy .
            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_file_path
                                                   )
                logging.info(response)
                return response

            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=False)
            return model_evaluation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")


# How can we get our best model ?  Wnen we will run our pipeline for the first time . Then the best location file will not be avaialble .

# We will check the model which is in production that's what we call it as retraining . Retraining means checking the new train model with the best model which is already present in the production . So, we create the pipeline in such a way that we will only send the model which will be better than the model which is in production . It is just like a check that we are doing from our side before pushing our model into the production . So, it will only send that model with which we will do retraining means comparing it with the best model which is present in the production .