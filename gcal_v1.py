
from __future__ import print_function
import httplib2
import os
import sys, getopt

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# my weather forecast machine
import andyweather

import datetime
from pyfiglet import Figlet


#python-dateutil to parse the ISO date formats
import dateutil.parser



#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def gt(dt_str):
    return dateutil.parser.parse(dt_str)

def main(weeksAhead=0):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # this returns the most recent past Sunday
    # datetime.datetime.today()-datetime.timedelta(days=datetime.datetime.today().weekday()+1)
    # figure out sunday
    if datetime.datetime.today().weekday() == 6:
        sunday = datetime.datetime.today()
    else:
        sunday = datetime.datetime.today()-datetime.timedelta(days=datetime.datetime.today().weekday()+1)

    # add or subtract weeks based on the passed parameter
    sunday = sunday + datetime.timedelta(weeks=weeksAhead)
    
    sundayiso = sunday.isoformat() + 'Z' # 'Z' indicates UTC time
   

    eventsResult = service.events().list(
        calendarId='primary', timeMin=sundayiso, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    #if not events:
    #    print('No upcoming events found.')

    # here's the NOAA URL for NYC, and get the weather in a nice array of date and forecast
    weatherurl = 'http://forecast.weather.gov/MapClick.php?lat=40.7273&lon=-73.9807&FcstType=dwml'

    # now go get the weather forecast.  Returns a list of lists
    # [[datetime], [forecast]]
    weatherArray = andyweather.getWeather(weatherurl)

    # days of week, in calendar display order, not Python order
    dow = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # I loooove me some big fonts
    f = Figlet(font='big')
    print(f.renderText("Maxwell Calendar"))

    # This loops through the week, starting on Sunday thru Saturday
    for i in range(7):
        currentday = sunday + datetime.timedelta(days=i)
        print("---------------------------", dow[i], currentday.date())

        # loop through all the calendar events and find ones that match the day to print
        for event in events:
            start = gt(event['start'].get('dateTime', event['start'].get('date')))
            end = gt(event['end'].get('dateTime', event['end'].get('date')))
            if start.date() == currentday.date():
                if start == end - datetime.timedelta(days=1): # All-day events have no time, and the end time is midnight the next day
                    print(event['summary'])
                else:
                    print(event['summary'], start.time().strftime("%I:%M%p"), "to", end.time().strftime("%I:%M%p") ) # show times in 12-hour AM/PM format, the %-I for trimmed hours doesn't work on Windows
    
        # loop through the weather array putting out the forecast
        for j in weatherArray:
            if j[0].date() == currentday.date():
                # NOAA sets the time at 6am for the morning forecast and 6pm for the evening
                if j[0].hour == 6:
                    print("   ... Morning:", j[1])
                elif j[0].hour == 18:
                    print("   ... Evening:", j[1])
                else:
                    print("   ... Forecast:", j[1])

            

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "next":
            main(1)
        elif sys.argv[1] == "previous":
            main(-1)
        else:
            main()
    else:
        main()
