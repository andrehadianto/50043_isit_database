import yaml
import logging
import utils.user as user
from utils.utils import run_command_bash

def analytics():
    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    with open('config/config.yml') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)
        
    user.init()
    user.ACCESS_KEY = CONFIG["AWS_CREDENTIALS"]["ACCESS_KEY"]
    user.SECRET_KEY = CONFIG["AWS_CREDENTIALS"]["SECRET_KEY"]
    user.KEY_PAIR = CONFIG["AWS_CREDENTIALS"]["KEY_PAIR"]
    user.KEY_PATH = CONFIG["AWS_CREDENTIALS"]["KEY_PATH"]

    ANALYTICS_SCRIPT = "scripts/analytics/analytics.sh"

    command = ['/bin/bash', ANALYTICS_SCRIPT, user.KEY_PATH, CONFIG["MASTER"]["IP"], CONFIG["MONGO"]["IP"], CONFIG["MYSQL"]["IP"]]
    
    run_command_bash(command)
    
    logging.info("Output files are stored in hdfs. Name node: %s" % (CONFIG["MASTER"]["DNS"]))
    logging.info("The output of the correlation coefficient can be found in /corr/ in the last part file.")
    logging.info("For more information, visit https://github.com/andrehadianto/50043_isit_database/tree/develop/#1-correlation")
    logging.info("Output of Task 2 can be found at /tfidf directory in hdfs")
    logging.info("For more information, visit https://github.com/andrehadianto/50043_isit_database/tree/develop/#2-tf-idf")



if __name__ == '__main__':
    analytics()