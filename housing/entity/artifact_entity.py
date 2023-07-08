# from artifact entity import named tuple
from collections import namedtuple

# We are defining output for data-ingestion component . And we are going to give some names the output that we are expecting from  data ingestion components .
DataIngestionArtifact = namedtuple("DataIngestionArtifact",["","",""])

# We have not defined DataIngestionArtifact in config-entity.py beacause it is for output component(artifact) that we will get . But in config-entity.py we have defined only input(configuration) for special components .So, as DataIngestionArtifact is output component that'sway we have created seperate file for it .

# So, by this we will seperately manage every file . If I will be working on output artifact I don't need to check my configuration file .

# The output for DataIngestionArtifact will be downloaded file, extract file , train file , test file . So, this can be the artifact .






