#metaWeather API usage

import requests
import json
import threading

'''Added the ability to find weather data by searching the API by city name and getting the WOEID so you don't have to know beforehand'''
locations = ['2487610', '2442047', '2366355', 'New York', 'Boston']

'''Searches by city name and returns WOEID'''
'''Included some basic exception handeling for both getting the url and getting the JSON data'''
def getWOEID(loc):
    url = 'https://www.metaweather.com/api/location/search/?query=' + loc
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Encountered an Error:', e, 'for', loc, '\nExiting...')
        quit()
    try:
        d = r.json()
    except json.decoder.JSONDecodeError:
        print('Encountered an Error decoding the JSON data for Location:', loc, 'Exiting...')
        quit()
    return(str(d[0]['woeid']))    

'''Returns JSON data for location'''
def getWeather(loc):
    url = 'https://www.metaweather.com/api/location/' + loc
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Encountered an Error:', e, 'for', loc, '\nExiting...')
        quit()
    try:
        d = r.json()
    except json.decoder.JSONDecodeError:
        print('Encountered an Error decoding the JSON data for Location:', loc, 'Exiting...')
        quit()
    return(d)

'''Adds max temps together and prints the avg out in F'''
def getAvgMax(loc):
    rawWeather = getWeather(loc)
    maxTemps = 0.0
    for i in range(6):
        maxTemps += rawWeather['consolidated_weather'][i]['max_temp']
    print(rawWeather['title'], 'Average Max Temps Over Next 5 days is:', str(round(CtoF(maxTemps/6), 2)), 'Farenheit')
    return()

'''Converts to Celcius to Farenheit'''
def CtoF(temp):
    return(temp*(9/5)+32)

'''Main process, loops over the location list, checks if its a number or a character string. If its a character string 
it will search for the city WOEID. Opens threads for each city in the list, calling GetAvgMax for each thread sending WOEID
as the arg. Joins the threads and exits the program.'''

def main():
    threads = []
    for j in locations:
        if j[1].isnumeric():
            x = threading.Thread(target = getAvgMax, args = (j, ))
        else:
            z = getWOEID(j.replace(' ', '+'))
            x = threading.Thread(target = getAvgMax, args = (z, ))
        threads.append(x)
        x.start()

    for k in threads:
        k.join()

    exit()

main()
