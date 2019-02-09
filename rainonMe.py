import requests
#import sys #TODO Command line input
from bs4 import BeautifulSoup
import traceback
from datetime import datetime

###########################################################
#                  GLOBAL VARIABLES                       #
###########################################################
debug = True  #For (gasp) debugging statements
forecasts = dict() #Dict to store forecasts


#TODO Turn into args inputs for modularity
#try:
    #lat = sys.argv[0]
    #lon = sys.argv[1]
#except:
    #print("Something went wrong. Please check inputs and try again")
    #exit()
lat = "41.657"
lon = "-91.5265"

def getTitles(weatherList):
    titles = []

    for item in weatherList:
        title = ''
        periodname = item.find(class_="period-name")

        for name in periodname.contents:
            if name.string is not None:
                title = title + name.string + " "

        titles.append(title.strip())
    return titles


#TODO Issue (A): Bad weather alert resulted in an additional container that was logged by BS4 without temp section. This caused errors in the below
#   function. Need to increase precison of web scraping to harden code.
def getTemps(weatherList):
    temps = []

    for item in weatherList:
        tempname = None

        if item.find(class_="temp temp-low") is not None:
            tempname = item.find(class_="temp temp-low")
        elif item.find(class_="temp temp-high") is not None:
            tempname = item.find(class_="temp temp-high")
        elif debug == True:
            print("Unable to find temperature within getTemps function. Attempting to log relevant HTML to rainonMe.log.")
            try:
                with open('rainonMe.log', 'a') as f:
                    f.write(datetime.now().strftime("%m_%d_%Y_%H_%M_%S-"))
                    f.write(item.prettify())
                    f.write('\n \n \n')
            except:
                print('Unable to log error within getTemps function.')
            finally:
                print('An exception is likely to be thrown.')
                temps.append('N/A')

        if tempname is not None:
            for content in tempname.contents:
                try:
                    if(content[0] == 'L' or content[0] == 'H'):
                        temps.append(content.string)
                except KeyError:
                    pass

    return temps

def getDescriptions(weatherList):
    short_desc = []

    for item in weatherList:
        desc = item.find(class_="short-desc")
        temp = ''

        for content in desc.contents:
            if content.string is not None:
                temp = temp + ' ' + content.string

        short_desc.append(temp.strip())
    return short_desc


### Main Thread ###
try:
    #Start by web scraping from National Weather Service
    response = requests.get("https://forecast.weather.gov/MapClick.php?lat=" + lat + "&lon=" + lon)
    if debug == True:
        print("Status code " + str(response.status_code))

except:
    if debug == True:
        print("Something went wrong. Exiting program.")
    traceback.print_exc()
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast-list")
forecast_items = seven_day.find_all(class_="tombstone-container")

#Pass forecast_items list to these 3 functions to pull out data into more specific lists of items
titles = getTitles(forecast_items)

temps = getTemps(forecast_items)

descs = getDescriptions(forecast_items)


for x in range(len(titles)):
    forecasts.update({x : [titles[x], temps[x], descs[x]]})

if debug == True:
    for x in range(3):
        first, second, third = forecasts[x]
        print(first)
        print(second)
        print(third + "\n")


if debug == True:
    print("!!! It worked!!! End of program!!!")