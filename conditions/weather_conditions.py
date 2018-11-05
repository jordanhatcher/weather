"""
weather_conditions
"""

import logging
from apscheduler.triggers.cron import CronTrigger
from pubsub import pub
from condition import Condition

LOGGER = logging.getLogger(__name__)

CONDITION_CLASS_NAME = 'WeatherConditions'

class WeatherConditions(Condition):
    """
    WeatherConditions

    Conditions for reading weather data
    """

    def __init__(self, scheduler, schedule='0 * * * *'):
        """
        Constructor
        """

        Condition.__init__(self, scheduler, schedule)
        scheduler.add_job(self.evaluate, CronTrigger.from_crontab(schedule))
        LOGGER.debug('Initialized')

    def evaluate(self, msg=None):
        """
        Handler for receiving messages
        """

        LOGGER.info('Evaluating')
        pub.sendMessage('weather.update', msg=None)
