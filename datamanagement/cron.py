import logging
from .models import *
from .views import *
import traceback

logger = logging.getLogger('dev_log')

def my_scheduled_job():
    logger.info("it started")
    user=strategy.objects.get(username="testing")
    try:
        do_something(user)
    except Exception:
        logger.info(str(traceback.format_exc()))
