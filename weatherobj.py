#metaWeather API usage

import requests
import json
import threading
from concurrent.futures import Future

def callFuture(func, future, args, kwargs):
    try:
        result  = func(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)

def threadFunc(func):
    def wrap(*args, **kwargs):
        future = Future()
        threading.Thread(target = callFuture, args = (func, future, args, kwargs)).start()
        return(future)
    return(wrap)


class weatherOBJ:
    '''As object is created, call a thread for the getWeather funciton for each location give,
    waits until all data has been received before moving on '''
    def __init__(self, loc):
        self.locations = {}
        for j in loc:
            self.locations[j] = self.getWeather(j)

        for k in self.locations.keys():
            self.locations[k] = self.locations[k].result()

    '''Returns JSON data for location, if a city name is submitted instead of a WOEID it will
    find the WOEID by searcing on the API. Fuction is threaded when called'''
    @threadFunc
    def getWeather(self, loc):
        if loc[1].isalpha():
            url = 'https://www.metaweather.com/api/location/search/?query=' + loc
            try:
                r = requests.get(url)
            except requests.exceptions.RequestException as e:
                print('Encountered an Error:', e, 'for', loc, 'Exiting...')
                return(None)
            try:
                d = r.json()
            except json.decoder.JSONDecodeError:
                print('Encountered an Error decoding the JSON data for Location:', loc, 'Exiting...')
                return(None)
            self.woeid = (str(d[0]['woeid']))
        else:
            self.woeid = loc

        url = 'https://www.metaweather.com/api/location/' + self.woeid
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            print('Encountered an Error:', e, 'for', loc, 'Exiting...')
            return(None)
        try:
            d = r.json()
        except json.decoder.JSONDecodeError:
            print('Encountered an Error decoding the JSON data for Location:', loc, 'Exiting...')
            return(None)
        return(d)

    '''Adds max temps together and prints the avg out in F'''
    def getAvgMax(self, loc):
        maxTemps = 0.0
        for i in range(6):
            maxTemps += int(loc['consolidated_weather'][i]['max_temp'])
        print(loc['title'], 'Average Max Temps Over Next 5 days is:', str(round(self.CtoF(maxTemps/6), 2)), 'Farenheit')
        return()

    '''Main handler function for processing requested data'''
    def getData(self, requestedData):
        if requestedData == 'getAvgMax':
            for loc in self.locations.keys():
                self.getAvgMax(self.locations[loc])
        else:
            print('Invalid Funciton Requested...')
            return()

    '''Converts to Celcius to Farenheit'''
    def CtoF(self, temp):
        return(temp*(9/5)+32)
