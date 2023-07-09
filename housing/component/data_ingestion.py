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
import pandas as pd 
import numpy as np

from sklearn.model_selection import StratifiedShuffleSplit
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
            # from e means it will tell that what error or exception is happening . If we don't write then it will tell line number 53 has exception .

    
    # Extracting zip file  and it will be converted to raw file. It give csv file .
    # We will first accept the tgz_file_path which is just a type of string .
    def extract_tgz_file(self,tgz_file_path:str):
        try:
            # Next task is to generate raw data dir .
            # Now we have to extract the tgz_data inside the raw_data .

            # I need the location where i will extract this file .
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            # Now if the above directory is not present then we need to create it .
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            
            os.makedirs(raw_data_dir,exist_ok = True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            # Next thing is that we have to read this tgz_file
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                # tgz_file_path is opened .
                housing_tgz_file_obj.extractall(path = raw_data_dir)
            logging.info(f"Extraction eompleted")


        except Exception as e:
            raise HousingException(e,sys) from e
    
    # Reading rqw file and split dataset into train dataset and test dataset
    def split_data_as_train_test(self):
        try:
            # first we need to know where our raw data dir . From config we can know where our raw data dir is .
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            # Now this is a directory but i need to know the file name .
            file_name = os.listdir(raw_data_dir)[0]
            
            # Now i want to complete csv file .
            housing_file_path = os.path.join(raw_data_dir,file_name)
            # so, we get complete file path .

            # Now if I want to read csv file then import pandas .
            # We are going to read this data frame .
            logging.info(f"Reading csv file: [{housing_file_path}]")
            housing_data_frame = pd.read_csv(housing_file_path)

            # refer notes
            # So, we will use this pd.cut function which will create category from the numerical column .
            housing_data_frame["income_cat"] = pd.cut(

            housing_data_frame["median_income"],bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
            # bins=[0.0,1.5,3.0,4.5,6.0,np.inf] , this is our category , so our data ranges between this . So, we have created the category of 1.5 factor .
            # Here median_income is column in our dataframe . Actually this median_income column will contain value form 0 to 50. 
            #So, we try to create bin for every thing .Mostly between 0 to 9 .
            # ouf target column is median_income because we want to create a category based on stratified split .

            lsbels=[1,2,3,4,5]
            # So, this will give us an extra column so that i can divide my dataset equally .

            )

            # Next thing is we want to create stratified train and test dataset .
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            # Next we have to import StratifiedShuffleSplit from sklearn

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            # here we want to create 1 split and test size is 20% and if we don't set random_state then also it is fine .
            
            for train_index,test_index in split.split(housing_data_frame,housing_data_frame["income-cat"]):

                # If we take the ratio between train_index and test_index based on income-cat , we will get the same .
                
                strat_train_set = housing_data_frame.loc[train_index].drop("income-cat",axis=1)
                # loc is used to extract row from  index location  by. So, in loc we will simply pass this train_index and drop this income-cat 
                # We wanted to drop this income-cat column that'sway we have taken axis =1 .
                strat_test_set = housing_data_frame.loc[train_index].drop("income-cat",axis=1)

            # Now, the next step is to save this dataset . 
            # We have directory of train dataset and test dataset and file_name ,sO, we will try to prepare train file path .
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok = True)
                logging.info(f"Exporging training dataset to file: [{train_file_path}]")
                # Now, we will save data-frame .
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok = True)
                logging.info(f"Exporting testing dataset to file: [{test_file_path}]")
                # here we will aslo save the data frame
                strat_test_set.to_csv(train_file_path,index=False)

            # Next thing is we just need to create data ingestion artifact .
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path, test_file_path=test_file_path,is_ingested=True,message=f"Data ingestion completed successfully.")

            # data_ingestion_artifact is the output which we have to provide .
            logging.info(f"Data ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact 



        except Exception as e:
            raise HousingException(e,sys) from e
    

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            # so, by using below mentioned function we will get the file location .
            tgz_file_path = self.download_housing_data()

            self.extract_tgz_file(tgz_file_path=tgz_file_path)

            return self.split_data_as_train_test()

        except Exception as e:
            raise HousingException(e,sys) from e

     # Whenever the object will destruct , we will run this function .   
    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20}\n\n")



# Configuration is all about providing the information . It is not about creating the folder or doing the task .

# In raw_data dir , we will our complete dataset but we will split that dataset into train and test dataset inside our  Data_ingestion folder .

# We just created additional column to split the data . And then I am droping the column as it is no more required .

# median_income is our target variable and i wanted to maintain the same distribution for median income only because of that we have created income_cat (income category).

# Any thing in bin if it is greater than 6.0 then i will consider it in label 5 .



