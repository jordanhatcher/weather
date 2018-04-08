"""
weather_node

Contains the WeatherNode class
"""

import json
import logging
import urllib.request
from pubsub import pub
from ....node import Node

LOGGER = logging.getLogger(__name__)

NODE_CLASS_NAME = 'WeatherNode'

OPEN_WEATHER_MAP_URL = 'http://api.openweathermap.org/data/2.5/weather'

class WeatherNode(Node):
    """
    WeatherNode

    Node providing an interface to weather data from openweathermap
    """

    def __init__(self, label, state, config):
        """
        Constructor
        """
        Node.__init__(self, label, state, config)

        pubsub.subscribe(self.update_state, f'{self.label}.update')

    def update_state(self):
        """
        Updates the node state. Fetches data from openweathermap and
        stores that data in the state object for the node.
        """

        weather = self._get_weather()
        self.state.update_states(self.label, **weather)

    def _get_weather(self):
        """
        Helper function to send a request to openweathermap to get the
        weather for the default city.
        """

        city = self.config['default_city']
        country = self.config['default_country']
        api_key = self.config['api_key']
        url = f'{OPEN_WEATHER_MAP_URL}?q={city},{country}&appid={api_key}'

        response = urllib.request.urlopen(url)
        text_response = response.read().decode('utf-8')
        weather = json.loads(text_response)['main']
        weather['temp'] = weather['temp'] - 273.15 # Kelvin to Celcius
