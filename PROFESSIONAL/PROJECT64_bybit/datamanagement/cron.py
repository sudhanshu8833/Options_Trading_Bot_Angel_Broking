

import logging
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')



def my_scheduled_job():
    print("Hello its working, my friend")
    logger.info("we have started logging... hurray!!")

