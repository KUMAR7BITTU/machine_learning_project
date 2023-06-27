from setuptools import setup
from typing import List

# Declaring variables for setup function
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="BITTU KUMAR"
DESCRIPTION="This is a first FSDS batch Machine Learning Project"
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:
    """
    Description: This file is going to return list of requirement
    mention in requirement.txt file .

    return This function is going to return a list which contain name of libraries mentioned in requirements.txt file 
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines()


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    package=PACKAGES,
    install_requires=get_requirements_list()
)

