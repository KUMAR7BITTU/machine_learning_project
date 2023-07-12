
# Here we will write code to check training and testing file is available or not .
# Because this is also one kind of validation , we have to make sure that our training file is available or not .If we have our training file then only i cna perform data transformation and data training .

# So,we have to create schema .


from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os,sys

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

import pandas as pd

import json 

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab 
# In DataValidation class , we also have to pass data ingestion artifact to validate it .
class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):

        # If we have only data_validation_config and DataValidationConfig because all the require configuration i can get from validation config  and training & testing file location i can get from output of data_ingestion (means data_ingestion_artifact) .
        try:
            # first we will take both the variable as instance variable 
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact 
        except Exception as e:
            raise HousingException(e,sys) from e
    
    # To get train and test dataset 
    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e



     # Before we do any validation i need to check my training and testing files are  available or not .   
    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            # first we will try to get our training and testing file path 
            is_train_file_exist = False
            is_test_file_exist = False

            # train and test file path are the output of data ingestion artifact phase 
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # os.path.exists() method in Python is used to check whether the specified path exists or not. 
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist
            
            logging.info(f"Is train and test file exists?-> {is_available}")

            if not is_available:

                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file : {training_file } or Testing file : {testing_file} is not present "
                raise Exception(message)
            
            return is_available
        except Exception as e:
            raise HousingException(e,sys) from e 
    
    
    # To validate schema dataset 
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            # Assignment validate training and testing dataset using schema file 
            # Number of Column 
            # Check the value of ocean proximity 
            # Check the column name
            
            validation_status = True
            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e
        
    # We are going to generate some validation report and based on that we can check there is data drift or not .
    # So, first we have to save the report .
    def get_and_save_data_drift_report(self):
        try:
            # First , i have to create a profile object
            profile = Profile(sections=[DataDriftProfileSection()])
            #  we have used Profile class here and in sections we have passed DataDriftProfileSection because we are working on data drift .

            # we need to have two data drift so that we can see the significant statisical difference between them. So, we need here test and train dataset .
            train_df,test_df = self.get_train_and_test_df()

            # In profile , we have calculate method and we will pass train & test dataset through which we can generate data drift report .
            profile.calculate(train_df,test_df)

            #profile.json()
            # All the data drift that has been calculate through profile , is available in the form of json file .
            
            # It will give dictionary and list as output
            report = json.load(profile.json())
            #The json.load() function takes a file-like object (such as an open file) as an argument and reads the JSON data from it. It then parses the JSON data and returns a Python object representing the data structure described in the JSON.

            # Now i want to sace this report in json file .
            with open(self,data_validation_config,report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)
            
            return report
            # Throug this report we can validate there is data drift or not .

        except Exception as e:
            raise HousingException(e,sys) from e
    

    def save_data_drift_report_page(self):
        try:
            # We need dashboard to see graphs
            # we need to create dashboard object and it require DataDriftTab in tab
            dashboard = Dashboard(tabs=[DataDriftTab()])

            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            dashboard.save(self.data_validation_config.report_page_file_path) # To save dashboard in required path
            
        except Exception as e:
            raise Exception(e,sys) from e

    # This is a function to check data drift
    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            is_available = self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path, report_file_path = self.data_validation_config.report_file_path, report_page_file_path=self.data_validation_config.report_page_file_path,is_validated = True,message="Data Validation Performed Successfully")
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")
        except Exception as e:
            raise HousingException(e,sys) from e 
        

# Data drift is nothing but our dataset statistic has changed now .

# We will see distribution both train and test dataset through evidently library , if there column distribution are align with each other(means train and test dataset ) then we can say that there is no data drift and if they are not align with each other we will say there will be data drift .

# We have to install one library called evidently .

# To generate the report we have to import two module (Profile and DataDriftProfileSection) or few classes from evidently library  to generate json kind of report on our dataset .

# Suppose previously we had some dataset , we will consider this dataset as our base dataset . Now, suppose we have to calculate data drift and now our dataset is changed , then we will compare the statistic of previous dataset with this newly changed dataset , to find that there is datadrift or not .
