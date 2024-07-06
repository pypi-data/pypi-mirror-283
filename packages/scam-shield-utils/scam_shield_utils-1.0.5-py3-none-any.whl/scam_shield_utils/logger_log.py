import json
import logging
import elasticapm
import elasticapm.handlers
from elasticapm.handlers.logging import LoggingHandler
from dotenv import load_dotenv
import os

import elasticapm.handlers.logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console_logger = None
load_dotenv()

client = None

def setup_loggers():

    # Get logger for console logging
    global console_logger

    console_logger = logging.getLogger("scamshield-scam-call-prediction")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #apm_formatter = LoggingHandler.format('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_logger.setLevel(logging.DEBUG)
    
    # Initialize Elastic APM agent
    apm_client = elasticapm.Client(
        service_name='scamshield-scam-call-prediction',
        secret_token=os.getenv('CALL_PREDICTION_APM_CRED_SECRET_TOKEN'),
        server_url=os.getenv('ELASTIC_APM_SERVER_URL'),
        verify_server_cert=parse_bool(os.getenv('CALL_PREDICTION_VERIFY_SERVER_CERT')),
        environment=os.getenv('CALL_PREDICTION_APM_CRED_ENVIRONMENT')
    )    

    global client
    client = apm_client  
    
    # Remove existing handlers to avoid duplicate logs
    for handler in console_logger.handlers[:]:
        console_logger.removeHandler(handler)
    # Configure console handler
    ch = logging.StreamHandler()
    #ch.setLevel(logging.INFO)  # Adjust level as needed
    ch.setFormatter(formatter)
    console_logger.addHandler(ch)
    # Configure file handler
    log_file_path = ""
    log_file_path=f"{os.getcwd()}\\call_prediction.log"

    fh = logging.FileHandler(log_file_path)  # Save logs into training.log file
    fh.setLevel(logging.INFO)  # Adjust level as needed
    fh.setFormatter(formatter)
    console_logger.addHandler(fh)

    # Configure APM handler
    apm_handler = LoggingHandler(apm_client)
    apm_handler.setLevel(logging.INFO)
    apm_handler.setFormatter(formatter)
    console_logger.addHandler(apm_handler)

    return console_logger

def parse_bool(value):
    """
    Parse boolean values from string.
    
    Args:
        value (str): String value to parse.

    Returns:
        bool: Boolean value parsed from the string.
    """
    return value.lower() == 'true' if value.lower() != 'false' else False

console_logger = setup_loggers()

#SUPPRESS_LOGS
suppress_messages = False #parse_bool(os.getenv('SUPPRESS_LOGS',False))

def log_message(log_level="info", message = ""):
    """Function for logging to the console and Elastic APM"""    
    # Log the message to the console
    if not suppress_messages:
        if log_level.lower() == "info":
            console_logger.info(message)
        elif log_level.lower() == "debug":
            console_logger.debug(message)        
        elif log_level.lower() == "error":
            console_logger.error(message)
        elif log_level.lower() == "warning":
            console_logger.warning(message)
        elif log_level.lower() == "critical":
            console_logger.critical(message)
        else:
            console_logger.info(message)

    return console_logger