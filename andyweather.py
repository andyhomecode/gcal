# Weather Module
# Andy Maxwell
# 8/6/2016
# v0.1
# Returns an list of days/weather [[date][weather]]

import urllib.request
import xml.etree.ElementTree as ET
import time
import sys
from datetime import datetime
#python-dateutil to parse the ISO date formats
import dateutil.parser

def getWeather(forecasturl):

    """Weather Fetcher

    Gets the weather when it's called and returns an array of arrays
    Returns an list of days/weather [[datedtime][weather forecast text]]    
    """

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

        #weathersummary = root.findall(".//data[@type='forecast']/parameters/weather/weather-conditions")[0].get('weather-summary')

        # the XML files have sections listing the times and dates for data like the descriptions
        # first get what format they're looking for.  It looks like this: k-p12h-n15-1
        timeLayout = root.findall(".//data[@type='forecast']/parameters/wordedForecast")[0].attrib["time-layout"]

        
        # I'll never remember what this xpath does next time I read this, sooooooooo
        # find the /data/time-layout/ that has an entry named layout-key with the right value we just found above
        # then get only the tags named start-valid-time.
        weatherDatesArrayXML = root.findall(".//data[@type='forecast']/time-layout[layout-key='" + timeLayout + "']/start-valid-time")

        weatherDatesArray =[]
        # Now we have an array with the dates and times the forecasts are for
        # and convert them to datetime objects
        for child in weatherDatesArrayXML:
            #print(child.tag, child.attrib, child.text)
            weatherDatesArray.append(dateutil.parser.parse(child.text))

        #for i in weatherDatesArray:
        #    print(i.day, i.month, i.year, i.hour)

        # Okay. Get the text for all the forecasts in an array
        weatherTextArrayXML = root.findall(".//data[@type='forecast']/parameters/wordedForecast/text")

        weatherTextArray = []
        for child in weatherTextArrayXML:
            weatherTextArray.append(child.text)
            #print(child.tag, child.attrib, child.text)

        #print(weatherTextArray)

        # final output container
        weatherArray = []
        for i in range(len(weatherTextArray)):
            j = []
            j.append(weatherDatesArray[i])
            j.append(weatherTextArray[i])
            weatherArray.append(j)

    except:
        # ruh roh
        print("Unexpected error:", sys.exc_info())

    return weatherArray


if __name__ == "__main__":
    print("Weather Module")

    #this is the NOAA URL for 10009
    print(getWeather('http://forecast.weather.gov/MapClick.php?lat=40.7273&lon=-73.9807&FcstType=dwml'))


