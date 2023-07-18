from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuartion
from housing.component.data_transformation import DataTransformation

def main():
   try:
       pipeline = Pipeline()
       pipeline.run_pipeline()
       # data_validation_config = Configuartion().get_data_validation_config()
       # print(data_validation_config)
    #    data_transformation_config = Configuartion().get_data_transformation_config()
    #    print(data_transformation_config)


   #  schema_file_path = r"C:/project_ml/machine_learning_project/config/schema.yaml"
   #  file_path = r"C:/project_ml/machine_learning_project/housing/artifact/data_ingestion/2023-07-10-12-26-12/ingested_data/train/housing.csv"

   #  df = DataTransformation.load_data(file_path = file_path, schema_file_path = schema_file_path)
   #  print(df.columns)
   #  print(df.dtypes)
    
   except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()