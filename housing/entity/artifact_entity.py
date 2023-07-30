# from artifact entity import named tuple
from collections import namedtuple

# We are defining output for data-ingestion component . And we are going to give some names the output that we are expecting from  data ingestion components .
DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path","test_file_path","is_ingested","message"])

# We have not defined DataIngestionArtifact in config-entity.py beacause it is for output component(artifact) that we will get . But in config-entity.py we have defined only input(configuration) for special components .So, as DataIngestionArtifact is output component that'sway we have created seperate file for it .

# So, by this we will seperately manage every file . If I will be working on output artifact I don't need to check my configuration file .

# The output for DataIngestionArtifact will be downloaded file, extract file , train file , test file . So, this can be the artifact .

# We need to define output . Right now , training file and test file is required for other component (like data validation) . So, we will try to take two to three properties like training file location and test file location so that it could be utilized for data transformation and data validation steps . One more output is whether it was successful or not along with we can also write some messages .


# So, now we will import this DataingestionArtifact in data_ingestion.py in component folder . Refer data_ingestion.py

DataValidationArtifact = namedtuple("DataValidationArtifact",["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])

# We are going to use this schema file in data transformation phase therefoee it is artifact . When i will load my dataset before doing feature engineering , to ensure that i have loaded my dataset properly along with their datatypes . In next phase when i will read my dataset , i will try to update the datatype of every column . for that we need schema file path . We need schema file for data transformation step that'sway i kept it here .

DataTransformationArtifact = namedtuple("DataTransformationArtifact",["is_transformed","message","transformed_train_file_path","transformed_test_file_path","preprocessed_object_file_path"])

# We require transformed_train_file_path and transformed_test_file_path because if we do training in our train and test dataset , then we will store those transformed train and test dataset in transformed_train_file_path and transformed_test_file_path respectively .

# When we try to create pickle of our transformed dataset then we will store that pickle file in preprocessed_object_file_path .


ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path", "train_rmse", "test_rmse", "train_accuracy", "test_accuracy", "model_accuracy"])

ModelEvaluationArtifact = namedtuple("ModelEvaluationArtifact", ["is_model_accepted", "evaluated_model_path"])

ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["is_model_pusher", "export_model_file_path"])
# ModelPusherArtifact will contain is_model_pusher which will tell is our model is pushed or not . Alongwith it will also contain export_model_file_path which will contain the location of where our model file path is located .