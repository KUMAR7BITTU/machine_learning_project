from housing.exception import HousingException
from housing.logger import logging
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.artifact_entity import DataValidationArtifact
from housing.entity.artifact_entity import DataTransformationArtifact

import sys,os
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from housing.util.util import read_yaml_file,save_object,save_numpy_array_data,load_data
# We have use save_object data because we want to save preprocessing object . When i have to transform my dataset then we have to use save numpy our array by using save_numpy_array_data . load data we require because we wanted to read data .

from housing.constant import *
import numpy as np
class FeatureGenerator(BaseEstimator,TransformerMixin):
    def __init__(self, add_bedrooms_per_room = True,total_rooms_ix = 3, population_ix = 5,households_ix = 6, total_bedrooms_ix = 4, columns = None):
        """
        FeatureGenerator Initialization
        add_bedroom_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of household columns
        total_bedrooms_ix: int index number of bedroom columns
        """
        try:
            logging.info(f"{'=' * 20}Data Transformation log started. {'=' *20} ")
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)
            
            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            raise HousingException(e,sys) from e

    def fit(self, X, y=None):
        return self
    
    def transform(self,X,y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                                 X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                                       X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                generated_feature = np.c_[X, room_per_household, population_per_household]

            return generated_feature
        except Exception as e:
            raise HousingException(e,sys) from e 

class DataTransformation:
    # we have to pass DataIngestionArtifact as a parameter as we want to know training and test file location. We also have to pass DataValidationArtifact as a parameter as we can get schema file from there .
    # At last it is compulsory to pass DataTransformationConfig here to use it's configuration here .
    def __init__(self,data_transformation_config:DataTransformationConfig, data_ingestion_artifact = DataIngestionArtifact, data_validation_artifact = DataValidationArtifact):
        try:
            # We have to store information in the function so that it can be utilized in data transformation step .
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        

    # We are going to return the object of ColumnTransformer which is going to combine both numerical and both categorical pipeline . So, that object we are going to create pickle .
    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            # We will get schema file path from data_validation_artifact
            schema_file_path = self.data_validation_artifact.schema_file_path
            
            # We can read the schema file
            dataset_schema = read_yaml_file(file_path = schema_file_path)
            # It will return us a dictionary .

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            num_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="median")), ('feature_generator',FeatureGenerator(add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room, columns = numerical_columns)),
                ('scaler', StandardScaler())
            ])


            cat_pipeline = Pipeline(steps=[
                ('impute',SimpleImputer(strategy="most_frequent")),
                ('one_hot_encoder',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean = False))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")
            

            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns)
            ])


        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object")
            # It can bring preprocessing object 
            preprocessing_obj = self.get_data_transformer_object()

            # Next is we need dataframe so that we can call data transformation object .
            # We have to get training dataframe file path from data ingestion artifact .
            logging.info(f"Obtaining training and test file path .")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Then we have to load our dataset .
            schema_file_path = self.data_validation_artifact.schema_file_path
            logging.info(f"Loading training and test data as pandas dataframe")
            train_df = load_data(file_path = train_file_path, schema_file_path = schema_file_path)
            # This will give us training dataset .

            test_df = load_data(file_path = test_file_path, schema_file_path = schema_file_path)

            # We also have to read schema 
            schema = read_yaml_file(file_path = schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]
            # Above code will give us median_housing_value

            # We are splitting our input and target feature on training dataset .
            logging.info(f"Splitting input and target feature from training and testing dataframe. ")
            input_feature_train_df= train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns = [target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            # from above code we got our training and test array

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            # So we will be able to make our training and test array and with the help of transformation we can concatenate our target feature .

            # Next is we want to save this train and test array .
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")
            
            transformed_train_file_path = os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir,train_file_name)

            logging.info(f"Saving transformed training and testing array. ")
            save_numpy_array_data(file_path = transformed_train_file_path, array = train_arr )
            save_numpy_array_data(file_path = transformed_test_file_path, array = test_arr)
            
            # Save our preprocessing object file path .
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            
            logging.info(f"Saving preprocessing object. ")
            save_object(file_path = preprocessing_obj_file_path, obj = preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True, message = "Data transformation successful.",
            transformed_train_file_path = transformed_train_file_path,     
            transformed_test_file_path = transformed_test_file_path, preprocessed_object_file_path = preprocessing_obj_file_path
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'='*20}Data Transformation log completed. {'='*20} \n\n")

# We are doing OneHotEncoding , once we have done OneHotEncoding then everywhere we will have 1's or 0's somekind of that . Then we are just trying to apply standard scaling . We want every feature to be in the same scale . If we don't do it then our categorical column will get advantage as compared to the numerical column .

# If we want every column to be in same scale , then we have to apply standard scaling on categorical column also .

