#!/bin/env python

'''
Description: Script to get a city's current and tomorrow morning weather.

Prerequisite: openweathermap.org APIKEY. It should be stored in the environnement variable OPENWEATHERMAP_APIKEY.

Input:
     arg1 = city name.
     arg2 = country name.
     City and country names must respect the ISO 3166 country codes (https://www.iso.org/obp/ui/#search)
Output:
     city's current weather.

Examples:
openweathermap_api.py washington united-states
openweathermap_api.py kenitra morocco
'''

import requests
import json
from datetime import datetime, timedelta, timezone
import sys
import os

def get_APIKEY():
    try:
        global OPENWEATHERMAP_APIKEY
        OPENWEATHERMAP_APIKEY = os.environ['OPENWEATHERMAP_APIKEY']
    except KeyError:
        print("Could not find the OPENWEATHERMAP_APIKEY env. variable. Make sure it is set and exported.")
        sys.exit(1)
    else:
        return OPENWEATHERMAP_APIKEY

def get_coordinate_by_location (city_state):
    '''API doc: https://openweathermap.org/api/geocoding-api#direct'''
    geodata_payload = {'q': city_state, 'limit': 1, 'appid': OPENWEATHERMAP_APIKEY }
    try:
        r = requests.get('http://api.openweathermap.org/geo/1.0/direct', params=geodata_payload)
        r.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)
    response = json.loads(r.text)[0]
    return response['lat'],response['lon']

def get_current_weather(coordinates):
    '''API doc: https://openweathermap.org/current#one'''
    weather_payload = {'lat': coordinates[0], 'lon': coordinates[1], 
                       'appid': OPENWEATHERMAP_APIKEY, 'units': 'metric'}
    try:
        r = requests.get('https://api.openweathermap.org/data/2.5/weather', params=weather_payload)
        r.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(error)
        sys.exit(1)
    response = json.loads(r.text)
    print(f'######## "{response["name"]}" current weather #########')
    print(f'Weather: {response["weather"][0]["main"]} - {response["weather"][0]["description"]}')
    print(f'Temperature: {response["main"]["temp"]}')
    print(f'Humidity: {response["main"]["humidity"]}')
    print(f'Wind speed: {response["wind"]["speed"]}')


def get_tomorrow_morning_epoch(time):
    # Get the current date and time in UTC
    now_utc = datetime.now(timezone.utc)
    # Calculate the date and time for tomorrow at {time} AM in UTC
    tomorrow_utc = datetime(now_utc.year, now_utc.month, now_utc.day) + timedelta(days=1, hours=time)
    # Convert the datetime object to epoch timestamp
    tomorrow_utc_epoch = int(tomorrow_utc.replace(tzinfo=timezone.utc).timestamp())
    return int(tomorrow_utc_epoch)

def get_forecast_weather(coordinates,tomorrow_utc_time):
    '''API doc: https://openweathermap.org/forecast5'''
    weather_payload = {'lat': coordinates[0], 'lon': coordinates[1], 
                       'appid': OPENWEATHERMAP_APIKEY, 'units': 'metric', 'cnt': '24'}
    r = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=weather_payload)
    response = json.loads(r.text)
    #we get a list containing dict, we store it in list_reponse
    list_reponse = response['list']
    
    #get tomorrow UTC epoch
    tomorrow_utc = get_tomorrow_morning_epoch(tomorrow_utc_time)

    #search the list list_reponse, and store the dict corresponding to timestamp to dict_reponse
    for d in list_reponse:
        for value in d.values():
            if value == tomorrow_utc:
                dict_reponse_1 = d
    
    #Here is a nested dict inside the list weather, extract the dict to dict_reponse_2
    for d in dict_reponse_1.get('weather'):
        for value in d.values():
            dict_reponse_2 = d

    print(f'######## "{response["city"]["name"]}" tomorrow weather at {dict_reponse_1.get('dt_txt')} (UTC) #########')
    print(f'Weather: {dict_reponse_2.get('main')} - {dict_reponse_2.get('description')}')
    print(f'Temperature: {dict_reponse_1.get('main').get('temp')}')
    print(f'Humidity: {dict_reponse_1.get('main').get('humidity')}')
    print(f'Wind speed: {dict_reponse_1.get('wind').get('speed')}')

def arg_parser():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <city> <country>')
        sys.exit(1)
    else:
        location = ','.join([sys.argv[1],sys.argv[2]])
    return location

get_APIKEY()
city_coordinates = get_coordinate_by_location(arg_parser())
print(f'Coordinates are: {city_coordinates}')
get_current_weather(city_coordinates)
get_forecast_weather(city_coordinates,tomorrow_utc_time=9)
