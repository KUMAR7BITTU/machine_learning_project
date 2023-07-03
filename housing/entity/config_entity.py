from collections import namedtuple 

# Define structure for configuration in every component in pipeline .

DataIngestionConfig = namedtuple("DataIngestionConfig",["dataset_download_url","tgz_download_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"])


DataValidationConfig = namedtuple("DataValidationConfig",["schema_file_path"])

# schema_file_path will contain information about how many numbers of columns will be there and what will be there datatype . So, where this schema file will be located that file we will specify in DataValidationConfig .


DataTransformationConfig = namedtuple("DataTransformationConfig",["add_bedroom_per_room","transformed_train_dir","transformed_test_dir","preprocessed_object_file_path"])

# In dataformation step we are going to generate one pickle file . That pickle object of feature engineering that we are going to use in prediction pipeline .So, when i will create that pickle file , we will store the location at preprocessed_object_file_path . 

# We will apply feature engineering on dataset mentioned in ingested_train_dir then we will store the location of transformed  dataset in transformed_test_dir .

# Same thing happens for transformed_test_dir as mentioned above .

# As of now in our dataset , there is no add_bedroom_per_room column . So, if we want to add this column , then we will pass true in add_bedroom_per_room else pass false . It just we are just creating an extra column whose name is add_bedroom_per_room .

ModelTrainerConfig = namedtuple("ModelTrainerConfig",["trained_model_file_path","base_accuracy"])

# If we train a model then we create a pickle file from that trained model . So, we have to save that file somewhere .We can  specity the location by trained_model_file_path where we saved our file ..

# If suppose i am training a model and that model is not giving accuracy greater than base_accuracy then i will not accept that model .

# There is only one trained_model_file_path because if we have 2 to 3 models then we have to choose the best model from them . We have to train that specific model only that'sway we have only one trained_model_file_path .

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig",["model_evaluation_file_path","time_stamp"])

# We will keep information about all our existing models that we have in production in model_evaluation_file_path .So, whenever we will try to train our model , we will read this information .

# In model evaluation step ,we use test dataset to evaluate our model and we compare with the best model . The model that we have in production and the model which we are training , we have to compare or evaluate those model in modelevalutaion step .But we need information about the model which is in production so that information we will get through model_evaluation_file_path .

# At time we are comparing or evaluating our model , we have to store that information in time_stamp .

ModelPusherConfig = namedtuple("ModelPusherConfig",["export_dir_path"])
# After comparing our trained model with production model , suppose our trained model is better then we have to push our trained model in same folder where our production model was available and in export_dir_path .