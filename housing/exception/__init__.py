import os
import sys

class HousingException (Exception):
    def __init__(self,error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,error_detail=error_detail)


    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys):
        """
        error_message : Exception object
        error_details : object of sys module
        """
        _,_ ,exec_tb = error_detail.exc_info()

        line_number = exec_tb.tb_frame.f_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error occured in script: [{file_name}] at line number : [{line_number}] error_message: [{error_message}]"

        return error_message
    
    def __str__(self):
        return self.error_message
    
    # Whenever we try to print exception object then this __str__() function will run and we will be able to see print statement .
    

    def __repr__(self)-> str:
        return HousingException.__name__.str()
    # whenever we try to call housing exception then ___rep__() function will and we will get just the name housing exception .
    