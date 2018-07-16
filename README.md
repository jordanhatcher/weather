# Weather

This is a package for my automation system that provides an interface to
OpenWeatherMap to get weather data.

## Setup

Before setting up this package, an OpenWeatherMap API key is needed. A free API
key can be obtained [here](https://openweathermap.org/price).

To install this package, clone this repo in the `packages` directory for the
automation system. In the `config.yml` file, add the following under `nodes:`

```yaml
weather:
  node: weather.weather_node
  config:
    default_city: <YOUR_CITY>
    default_country: <YOUR_COUNTRY>
    units: <metric | imperial>
    api_key: <API_KEY>
```

and the following under `conditions`:

```yaml
weather.weather_conditions:
  #Optional schedule cron
  schedule: '0 * * * *'
```
