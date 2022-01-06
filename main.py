#metaWeather API usage

import requests
import json
import threading
import logging

def getWeather(loc):
    url = 'https://www.metaweather.com/api/' + loc
    r = requests.get(url)
    d = r.json()
    print("Got Weather for", d['title'])
    return(d)

def getAvgMax(loc):
    rawWeather = getWeather(loc)
    maxTemps = 0.0
    for i in range(6):
        maxTemps += rawWeather['consolidated_weather'][i]['max_temp']
    return(maxTemps/6)

locations = ['location/2487610/', 'location/2442047/', 'location/2366355/']
for j in locations:
    print(getAvgMax(j))