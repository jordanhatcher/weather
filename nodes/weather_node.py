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
        self.state.add_states(self.label, ['weather'])

        pub.subscribe(self.update_state, f'{self.label}.update')

    def update_state(self, msg=None):
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
        units = self.config['units']
        api_key = self.config['api_key']
        url = f'{OPEN_WEATHER_MAP_URL}?q={city},{country}&units={units}&appid={api_key}'

        response = urllib.request.urlopen(url)
        text_response = response.read().decode('utf-8')
        dict_response = json.loads(text_response)

        description = dict_response['weather'][0]
        temp_pressure_humidity = dict_response['main']
        wind = {'wind': dict_response['wind']}

        weather = {**description, **temp_pressure_humidity, **wind}

        if 'rain' in dict_response:
            weather['rain'] = dict_response['rain']
        if 'snow' in dict_response:
            weather['snow'] = dict_response['snow']

        LOGGER.debug(weather)
        weather = {'weather': weather}
        return weather
