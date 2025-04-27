import sys

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    '''
    error_detail.exc_info() returns a tuple of three values:
        exc_type -> the exception type (e.g., ValueError, TypeError, etc.)
        exc_value -> the actual exception instance
        exc_traceback -> a traceback object (used to get details like filename, line number, etc.)
    '''
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message 
class CustomException(Exception):   # Custom exception class inheriting the Exception class
    def __init__(self, error_message, error_detail: sys):
        detailed_message = error_message_detail(error_message, error_detail)  # ✅ get the full error message
        super().__init__(detailed_message)  # ✅ pass the detailed message to Exception
        self.error_message = detailed_message  # store it in self too

    def __str__(self):
        return self.error_message
