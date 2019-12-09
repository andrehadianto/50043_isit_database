import yaml
import logging
import utils.user as user
from utils.utils import del_security_group, terminate_instances

# from utils.utils import 

def clean():
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

    instance_ids = [CONFIG["MASTER"]["ID"], CONFIG["FLASK"]["ID"]]
    # instance_ids = [CONFIG["MASTER"]["ID"], CONFIG["FLASK"]["ID"], CONFIG["MYSQL"]["ID"], CONFIG["MONGO"]["ID"]]
    for i in CONFIG["SLAVES"]:
        instance_ids.append(i["ID"])

    logging.info("Terminating instances...")
    
    terminate_instances(instance_ids)

    logging.info("Deleting security groups...")

    for id in CONFIG["SECURITY_GROUPS"]:
        del_security_group(id)

    open('config/config.yml', 'w').close()

    logging.info("Cleaned up!")

if __name__ == '__main__':
    clean()