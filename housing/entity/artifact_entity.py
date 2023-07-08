# from artifact entity import named tuple
from collections import namedtuple

# We are defining output for data-ingestion component . And we are going to give some names the output that we are expecting from  data ingestion components .
DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path","test_file_path","is_ingested","message"])

# We have not defined DataIngestionArtifact in config-entity.py beacause it is for output component(artifact) that we will get . But in config-entity.py we have defined only input(configuration) for special components .So, as DataIngestionArtifact is output component that'sway we have created seperate file for it .

# So, by this we will seperately manage every file . If I will be working on output artifact I don't need to check my configuration file .

# The output for DataIngestionArtifact will be downloaded file, extract file , train file , test file . So, this can be the artifact .

# We need to define output . Right now , training file and test file is required for other component (like data validation) . So, we will try to take two to three properties like training file location and test file location so that it could be utilized for data transformation and data validation steps . One more output is whether it was successful or not along with we can also write some messages .


# So, now we will import this DataingestionArtifact in data_ingestion.py in component folder . Refer data_ingestion.py



