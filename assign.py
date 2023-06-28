import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from collections import defaultdict

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = "18MYt45bq_UjoAKP-cQjg5nVeyAXaC7lpC_CsUIKXJns"


def assign_rides_back():
    
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Current!B2:H100").execute()
        values = result.get('values', [])

        #get values
        early = []  #all areas just grouped in here
        areas = defaultdict(list)  #mesa, middle, plaza, vdc/vdcn, puerta, off campus
        for row in values:
            #divide into early and fellowship
            if row[5]=='NO':
                early.append((row[0], row[4]))
            else:
                #mesa
                if 'mesa' in row[4].lower():
                    areas['mesa'].append((row[0], row[4]))
                elif 'brandy' in row[4].lower() or 'middle' in row[4].lower():
                    areas['middleearth'].append((row[0], row[4]))
                elif 'plaza' in row[4].lower():
                    areas['plaza'].append((row[0], row[4]))
                elif 'vdc' in row[4].lower():
                    areas['vdcvdcn'].append((row[0], row[4]))
                elif 'puerta' in row[4].lower():
                    areas['vdcvdcn'].append((row[0], row[4]))
                else:
                    areas['offcampus'].append((row[0], row[4]))

        # for k, v in areas.items():
        #     print(k, len(v))
        #     print(v)
        #     print()

        return areas

    except HttpError as err:
        print(err)