from housing.config.configuration import configuartion
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.config_entity import DataIngestionConfig
from housing.component.data_ingestion import DataIngestion

import os,sys

# To run this pipeline we have to call object of this Pipeline class and then with the help of object we have to execute different function mentioned in that class .

class Pipeline:

    def __init__(self,config:  configuartion)->None:
        try:
            self.config=config
            
        except Exception as e:
            raise HousingException(e,sys) from e 
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            # Now we have to create data ingestion object
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            
            # We have written this function  to download data and extract data  and it will return DataIngestionArtifact . So, we can directly return it .
            data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise HousingException(e,sys) from e
    

    def start_data_validation(self):
        pass

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
         pass
    
    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass
    

    # function to run pipeline 
    def run_pipeline(self):
        try:
            # data ingestion
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e 


