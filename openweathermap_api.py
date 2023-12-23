#!/bin/env python

'''
Description: Script to get a city's current weather.

Prerequisite: openweathermap.org APIKEY. It should be stored in the environnement variable OPENWEATHERMAP_APIKEY.

Input:
     arg1 = city name.
     arg2 = country name.
Output: city's current weather.

City and country names must respect the ISO 3166 country codes (https://www.iso.org/obp/ui/#search)

Examples:
openweathermap_api.py washington united-states
openweathermap_api.py kenitra morocco
'''

import requests
import json
import datetime
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


# def get_epoch_of_tomorrow_at_x(time):    
#     # Set the time to tomorrow at {time}
#     x_time = datetime.datetime.combine(datetime.datetime.utcnow().date() + datetime.timedelta(days=1), datetime.time(time))
#     # Convert the datetime object to a Unix timestamp
#     return int((x_time - datetime.datetime(1970, 1, 1)).total_seconds())

# def get_forecast_weather(coordinates):
#     '''API doc: https://openweathermap.org/forecast5'''
#     weather_payload = {'lat': coordinates[0], 'lon': coordinates[1], 
#                        'appid': OPENWEATHERMAP_APIKEY, 'units': 'metric', 'cnt': '24'}
#     r = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=weather_payload)
#     response = json.loads(r.text)
#     w = response['list']
#     print(f'######## "{response["city"]["name"]}" tomorrow weather #########')
#     ts = get_epoch_of_tomorrow_at_x(9)
#     if ts in w:
#         print("yes")
#     print(f'Weather: {w[0]["weather"][0]["main"]} - {w[0]["weather"][0]["description"]}')
#     # print(f'Temperature: {response["main"]["temp"]}')
#     # print(f'Humidity: {response["main"]["humidity"]}')

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
# get_forecast_weather(city_coordinates)
