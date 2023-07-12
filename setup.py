from setuptools import setup, find_packages
from typing import List

# Declaring variables for setup function
PROJECT_NAME = "housing-predictor"
VERSION = "0.0.2"
AUTHOR = "BITTU KUMAR"
DESCRIPTION = "This is the first FSDS batch Machine Learning Project"
PACKAGES = ["housing_predictor"]
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements_list() -> List[str]:
    """
    Returns a list of requirements mentioned in requirements.txt file.
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirements = requirement_file.readlines()
    return [req.strip() for req in requirements if "-e." not in req]


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()
)
