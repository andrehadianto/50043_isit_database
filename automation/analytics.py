import os
import yaml
import logging
import utils.user as user
import time
from utils.utils import run_command_bash

def analytics():

    LOG_PATH = os.path.join("config", "analytics_log.log")

    # Set up logging
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    fh = logging.FileHandler(LOG_PATH, mode='w')

    formatter = logging.Formatter('%(levelname)s: %(asctime)s: %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    with open('config/config.yml') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)
        
    user.init()
    user.ACCESS_KEY = CONFIG["AWS_CREDENTIALS"]["ACCESS_KEY"]
    user.SECRET_KEY = CONFIG["AWS_CREDENTIALS"]["SECRET_KEY"]
    user.KEY_PAIR = CONFIG["AWS_CREDENTIALS"]["KEY_PAIR"]
    user.KEY_PATH = CONFIG["AWS_CREDENTIALS"]["KEY_PATH"]

    ANALYTICS_SCRIPT = "scripts/analytics/analytics.sh"

    analytics = ['/bin/bash', ANALYTICS_SCRIPT, user.KEY_PATH, CONFIG["MASTER"]["IP"], CONFIG["MONGO"]["IP"], CONFIG["MYSQL"]["IP"]]
    
    run_command_bash(analytics)
    
    logger.info("Output files are stored in hdfs. Name node: %s" % (CONFIG["MASTER"]["DNS"]))
    logger.info("The output of the correlation coefficient can be found in /corr/ in the last part file.")
    logger.info("For more information, visit https://github.com/andrehadianto/50043_isit_database/tree/develop/#1-correlation")
    logger.info("Output of Task 2 can be found at /tfidf directory in hdfs")
    logger.info("For more information, visit https://github.com/andrehadianto/50043_isit_database/tree/develop/#2-tf-idf")



if __name__ == '__main__':
    analytics()