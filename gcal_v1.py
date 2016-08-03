
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

#python-dateutil to parse the ISO date formats
import dateutil.parser


# todo incorporate the weather objects
# get the weather from noaa
# parse it into an object that looks like this:
#
# forecast
#    days[0..6]
#        [datetime, textForecast]

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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

def convertdate(textdate):
    """Convert Google formatted date string into Python date string

    Andy's amazing date converter
    2016-08-01T11:00:00-04:00
    to a Python format
    """
    formatteddatetime = datetime.strptime('2016-08-01T11:00:00-04:00', '%b %d %Y %I:%M%p')
    return formatteddatetime


def gt(dt_str):
    return dateutil.parser.parse(dt_str)

def main():
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
    
    sundayiso = sunday.isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=sundayiso, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')

    # days of week, in calendar display order, not Python order
    dow = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    for i in range(7):
        currentday = sunday + datetime.timedelta(days=i)
        print(i, currentday, dow[i])
        

    for event in events:
        start = gt(event['start'].get('dateTime', event['start'].get('date')))
        end = gt(event['end'].get('dateTime', event['end'].get('date')))
        
        #print(start, end, event['summary'])
        # All-day events have no time, and the end time is midnight the next day
        if start == end - datetime.timedelta(days=1):
            print ("all day")
            

if __name__ == '__main__':
    main()
