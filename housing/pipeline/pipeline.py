from housing.config.configuration import configuartion
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.config_entity import DataIngestionConfig

import os,sys

class Pipeline:

    def __init__(self,config: configuartion = configuartion)->None:
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
        
    
    # function to run pipeline 
    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e
