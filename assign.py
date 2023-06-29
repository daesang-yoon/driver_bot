import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from collections import defaultdict
import random


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = "18MYt45bq_UjoAKP-cQjg5nVeyAXaC7lpC_CsUIKXJns"


def assign_rides_back():
    try:
        sheet = get_sheet()
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

        for k, v in areas.items():
            print(k, len(v))
            print(v)
            print()

        return areas    

    except HttpError as err:
        print(err)


def assign_rides_going():
    try:
        sheet = get_sheet()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Current!B2:H100").execute()
        values = result.get('values', [])

        #get values in the sheet
        people = []
        for row in values:
            if len(row[0])>5:
                index = row[0].rfind(' ')
                if index==-1:
                    people.append(row[0])
                else:
                    people.append(row[0][:index])
            else:
                people.append(row[0])

        #clear cells in previous ride assignement
        clear_cells(11, 8, "A1:K8", sheet)
        
        #account for too many sign ups for # of drivers
        if 4*len(drivers) < len(people):
            return 'not enough cars to take everyone'

        #make the list of lists for the rides sheet (all random)
        drivers = ['heidi', 'jessica', 'elliot', 'joel', 'erik', 'camryn', 'alex park']
        output = []
        header = ['GOING']
        header.extend(['']* (len(drivers)-1) )
        output.append(header)
        output.append([''])

        for d in drivers:
            output[1].append(d)
        
        while len(people) > 0:
            temp = ['']
            for i in range(0, len(drivers)):
                if len(people)==0:
                    break
                else:
                    rand_index = random.randint(0, len(people)-1)
                    temp.append(people[rand_index])
                    del people[rand_index]
            output.append(temp)


        # for o in output:
        #     print(o)

        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="rides!A1:K100",
                             valueInputOption="USER_ENTERED", body={"values": output}).execute()


        return 'updated spreadsheet on the rides tab for GOING rides'

    except HttpError as err:
        print(err)


def get_sheet():
    
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
        return sheet
    except HttpError as err:
        print(err)


def clear_cells(width, height, custom_range, sheet):  
    try:
        empty = []
        for i in range(height):
            empty.append([])
        for e in empty:
            for i in range(width):
                e.append('')

        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"rides!{custom_range}",
                             valueInputOption="USER_ENTERED", body={"values": empty}).execute()
       
    except HttpError as err:
        print(err)


assign_rides_back()
assign_rides_going()