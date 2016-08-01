import urllib.request
import xml.etree.ElementTree as ET
import time
import sys
from pyfiglet import Figlet
from datetime import datetime

# clear the screen
#print("\033c")

#wordedForecast = ""

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 1!!!!!!!!!!!!! DOES NOT WORK YET !!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# make it big
#f = Figlet(font='roman')


def getWeather():

    #this is the NOAA URL for 10009
    forecastUrl = 'http://forecast.weather.gov/MapClick.php?lat=40.7273&lon=-73.9807&FcstType=dwml'

    try:
        response = urllib.request.urlopen(forecastUrl)
        weatherxml = response.read()

        # print(weatherxml)            
        root = ET.fromstring(weatherxml)


        # get the time-layout, layout-key layout-key>k-p12h-n14-1 all of them for the 12-hour cuts
        
        # get the wordedForecast into an array
        # combine those two arrasy so it's [dateTime, wordedForecast]
        # sort by dateTime (should be already, but better safe than sorry
        # Somehow get it into an array with [date][am forecast][pm forecast]
        

        # !!!!!!!!!!!!!!!!!  BELOW HERE NOT EDITED YET !!!!!!!!!!!!!!!
        
        #gave up trying to find it using the string parser, here's the numbers
        lotemp = root.findall(".//data[@type='forecast']/parameters/temperature[@type='minimum']/value")[0].text
        #print(lotemp)
        
        hitemp = root.findall(".//data[@type='forecast']/parameters/temperature[@type='maximum']/value")[0].text
        #print(hitemp)

        currenttemp = root.findall(".//data[@type='current observations']/parameters/temperature[@type='apparent']/value")[0].text



        #weather type
        #weathersummary = root[1][5][3][1].get('weather-summary')
        weathersummary = root.findall(".//data[@type='forecast']/parameters/weather/weather-conditions")[0].get('weather-summary')

        weathertype = weathersummary
        # print(weathertype)
        
        # ditch all verbage
        verbage = ["Likely", "Breezy","Heavy","Mostly","Somewhat","Partly","Sky","Light", "Chance", "then", "and"]

        for i in verbage:
            weathertype = weathertype.replace(i, "")

        #and get rid of double spaces left over
        for i in range(10):
            weathertype = weathertype.replace("  ", " ")

        weathertype = weathertype.lstrip()
        weathertype = weathertype.rstrip()

        # http://graphical.weather.gov/xml/xml_fields_icon_weather_conditions.php
        # important weather terms listed in order of importance, most important last
        # If one of these terms shows up, it'll be the one displayed, last has precidence. Fog then Thunderstorm will be just Thunderstorm

        importantweather = ["Sunny", "Cloudy", "Drizzle", "Fog", "Frost", "Ice", "Showers", "Rain", "Flurries", "Snow", "Sleet", "Blizzard", "Thunderstorm", "Tstms", "T-storms", "Wintry"]


        for i in importantweather:
            if i in weathersummary:
                weathertype = i

        #sometimes forecasts are long.  Just grab the last word.  Close enough
        weatherwords = weathertype.split(" ")
        if len(weatherwords) > 1:
            lastweatherword = weatherwords[len(weatherwords)-1]
        else:
            lastweatherword = weatherwords[0]

        #print(lastweatherword)
        

        # ------------------------  START OF wordedForecast
        # get the text forecast
        wordedForecast = root.findall(".//data[@type='forecast']/parameters/wordedForecast/text")[0].text
        # if you got it put a smiley face in front
        print("--NETWORK UPDATE SUCCESSFUL--")

    except:
        # ruh roh
        print("Unexpected error:", sys.exc_info())
        wordedForecast = ""


       # format the stuff for output
    shortweather = '{0} {3} {1}/{2}'.format(currenttemp, lotemp, hitemp, lastweatherword)

    f = Figlet(font='alphabet')
    print(f.renderText(shortweather))

    # either the most recent forecast
    print(wordedForecast)

    # wait a minute and put dots across the bottom
    for i in range(60):
        print(".", end="", flush=True)
        time.sleep(1)
    print("!")

