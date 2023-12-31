from flask import Flask
import sys
from housing.logger import logging
from housing.exception import HousingException
app=Flask(__name__)

@app.route("/",methods=['GET','post'])
def index():
    try:
        raise Exception("We are testing custom exception")
    except Exception as e:
        raise HousingException(e,sys) from e
        logging.info(housing.error_message)
        logging.info("we are testing logging module")
    return "Starting Machine Learning Project"

if __name__=="__main__":
    app.run(debug=True)