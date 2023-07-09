from housing.entity.config_entity import DataIngestionConfig
import sys,os
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact

# We need some other library to extract the tar file .So, first we have to import tar file .Tar file is nothing but a compressed file .
import tarfile

# To download a file, we can use six.moves (module) and import library urllib.
from six.moves import urllib
# With the help of this library we cand dowmload data . With the help of tarfile we can extract the zip file .
class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e
    
    # Dowing housing dataset 
    def download_housing_data(self,)->str:
        try:
           # We have to download url
           # extraction remote url to download section .
           download_url = self.data_ingestion_config.dataset_download_url

           # folder location to download file
           tgz_download_dir = self.data_ingestion_config.tgz_download_dir

           # If suppose we have created this folder previously for for some project then we have to now use this folder for our current project then we have to first remove this folder .
           if os.path.exists(tgz_download_dir):
               os.remove(tgz_download_dir)

           # Suppose this tgz_download_dir folder where we will store tgz_download_dir is not available then we have to create it and if it is available then it is ok .
           os.makedirs(tgz_download_dir,exist_ok = True)

           # Next we have to extract file name housing.tgz from the url .
           housing_file_name = os.path.baseman(download_url)

           # Next I have to prepare our fullfile path for our zip file where we will download .
           tgz_file_path = os.path.join(tgz_download_dir,housing_file_name)

           logging.info(f"Downloading file from : [{download_url}] into :[{tgz_file_path}]")
           # Now we can use urllib to download the files form given the url .
           urllib.request.urlretrieve(download_url,tgz_file_path)
           logging.info(f"File :[{tgz_file_path}] has been downloaded successfully ")

           # Now we have to return the file path .
           return tgz_file_path



        except Exception as e:
            raise HousingException(e,sys) from e 
    
    # Extracting zip file  and it will be converted to raw file. It give csv file .
    def extract_gz_file(self,):
        pass
    
    # Reading rqw file and split dataset into train dataset and test dataset
    def split_data_as_train_test(self):
        pass
    

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            # so, by using below mentioned function we will get the file location .
            tgz_file_path = self.download_housing_data()
        except Exception as e:
            raise HousingException(e,sys) from e
        



        # Configuration is all about providing the information . It is not about creating the folder or doing the task .