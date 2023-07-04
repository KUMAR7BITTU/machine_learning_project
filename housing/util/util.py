# We will write some function in util and we will use those function whenever it will be required .
# Also we have yaml to read yaml file .

import yaml
from housing.exception import HousingException
import os,sys

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
    