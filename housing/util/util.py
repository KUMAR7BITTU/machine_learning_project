# We will write some function in util and we will use those function whenever it will be required .
# Also we have yaml to read yaml file .

import yaml
from housing.exception import HousingException
import os,sys
import numpy as np
import dill
import pandas as pd
from housing.constant import *

# We have created our custom Exception . so, we will use our custom Exception .

def read_yaml_file(file_path:str)->dict:
    """
    Read the yaml file and returns the contents as a dictionary.file_path: str

    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    

    # But actually this function is not a part of our main pipeline code .Just to read configuration yaml file . It's just kind of helper function .
    
    # Whenver we will try to create any helper function , we will write those function in util.py file  . functions like how to create pickle object , how to load a model in pickle object . These kind of function we will write in utill.py file .


    # Q, what is the use of util.py file ?
    # Ans:- There will be some functionalities which will not be a part of any pipeline . But it is required in multiple places , so we write those functions at util.py file . Like reading yaml file , creating pickle of object , reading of pickle object because that can be used in multiple places . reading yaml file is not a part of pipeline but still it is required .

    # We will use read_yaml_file function in configuration.py file  .
    
# After transformation we are getting data in array form . So, we need to save this array data .
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file 
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e
    
# Saving and loading of pickle file .
def save_object(file_path: str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e 
    
def load_object(file_path: str):
    """
    file_path: str
    """
    try: 
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e     

# We can pass file path and schema file path.
# We will try to write a function which will chcek datatypes and based on the datatypes it will convert those dataypes properly based on schema . In schema file we will read the column name and we will try to convert their datatypes .
@staticmethod
def load_data(file_path: str,schema_file_path: str)->pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)
        # dataset_schema will contain entire content of schema_file_path in dictionary format .
            
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
            

        # Now, we will read the dataframe
        dataframe = pd.read_csv(file_path)

        error_message = ""
        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \nColumn: [{column}] is not in the schema ."        
        if len(error_message) > 0:
            raise Exception(error_message)
        return dataframe


    except Exception as e:
        raise HousingException(e,sys) from e 

