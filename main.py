from __future__ import print_function
import datetime
import logging
import time
import sys
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def connect_to_cal(credentials_filename):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_filename, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_calendar_event_ids(captured_filename):
    calendar_event_ids = {}
    try:
        file = open(captured_filename, 'rb')
        calendar_event_ids = pickle.load(file)
        file.close()
        logging.info('captured_events file loaded')
    except:
        logging.info('No file loaded')
    return calendar_event_ids

def save_calendar_event_ids(calendar_event_ids, captured_filename):
    file = open(captured_filename, 'wb')
    pickle.dump(calendar_event_ids, file)
    file.close()

def print_event(cal, event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    summary = event.get('summary', 'private')
    attendees = 'unknown'
    if 'attendees' in event:
        attendees = [x['email'] for x in event['attendees']]

    s = cal + '\t' + start + '\t' + summary #+ '\t' + str(attendees[0:5])
    print(s)

def main():
    logging.basicConfig(format="%(asctime)s\t%(levelname)s\t%(message)s", level=logging.INFO)
    with open(sys.argv[1]) as config_file:
        config = json.load(config_file)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now_plus = (datetime.datetime.utcnow() + datetime.timedelta(days=20)).isoformat() + 'Z' # 'Z' indicates UTC time
    calendar_event_ids = get_calendar_event_ids(config['captured_filename'])

    service = connect_to_cal(config['credentials_filename'])
    logging.info('Connected to calendar')
    while (True):
        logging.info('new checking')
        new_events = False
        for cal in config['calendar_ids']:
            events = service.events().list(calendarId=cal, timeMin=now, timeMax=now_plus,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute().get('items', [])
            if cal not in calendar_event_ids:
                calendar_event_ids[cal] = set()
            for event in events:
                if event['id'] not in calendar_event_ids[cal]:
                    new_events = True
                    print_event(cal, event)
                    calendar_event_ids[cal].add(event['id'])
        if new_events:
            save_calendar_event_ids(calendar_event_ids, config['captured_filename'])
            print()

        time.sleep(60*config['check_interval_min'])


if __name__ == '__main__':
    main()
