How to use:

from currenttemperature.api import OpenMeteo, OpenWeather

open_meteo_obj = OpenMeteo(latitude,longitude)
print(open_meteo_obj.get_weather_temp())

open_weather_obj = OpenWeather(latitude,longitude,token_id)
print(open_weather_obj.get_weather_temp())