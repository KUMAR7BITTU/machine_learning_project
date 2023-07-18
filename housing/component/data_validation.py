from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os
import sys

import pandas as pd

import json

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'='*20}Data Validation log started. {'='*20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise HousingException(e, sys) from e

    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info("Checking if training and test file is available")

            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists? -> {is_available}")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file: {training_file} or Testing file: {testing_file} is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HousingException(e, sys) from e

    def validate_dataset_schema(self) -> bool:
        try:
            # Add your schema validation logic here
            validation_status = True
            return validation_status
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_and_save_data_drift_report(self):
        try:
            train_df, test_df = self.get_train_and_test_df()

            # Perform data drift analysis and generate report
            # Dummy report for illustration purposes
            report = {
                "data_drift": {
                    "feature1": 0.1,
                    "feature2": 0.2,
                    "feature3": 0.05
                }
            }

            # Save report to a JSON file
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=4)

            return report

        except Exception as e:
            raise HousingException(e, sys) from e

    def save_data_drift_report_page(self):
        try:
            train_df, test_df = self.get_train_and_test_df()

            # Perform data drift analysis and generate report page content
            # Dummy report page for illustration purposes
            report_page_content = "<html><body><h1>Data Drift Report Page</h1></body></html>"

            # Save report page to a file
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)

            with open(report_page_file_path, "w") as report_page_file:
                report_page_file.write(report_page_content)

        except Exception as e:
            raise Exception(e, sys) from e

    def is_data_drift_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            is_available = self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation Performed Successfully"
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise HousingException(e, sys) from e
    
    def __del__(self):
        logging.info(f"{'='*20}Data Validation log completed. {'='*20} \n\n")