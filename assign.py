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

#helper functions for list of drivers
def add_driver_going(driver):
    try:
        sheet = get_sheet()
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B1:M1").execute().get('values', [])[0]
        drivers = set(drivers)
        drivers.add(driver)
        drivers = list(drivers)
        clear_cells(12, 1, 'drivers!B1:M1', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="drivers!B1:M1",
                             valueInputOption="USER_ENTERED", body={"values": [drivers]}).execute()
    except HttpError as err:
        print(err)
def add_driver_returning(driver):
    try:
        sheet = get_sheet()
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B3:M3").execute().get('values', [])[0]
        drivers = set(drivers)
        drivers.add(driver)
        drivers = list(drivers)
        clear_cells(12, 1, 'drivers!B3:M3', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="drivers!B3:M3",
                             valueInputOption="USER_ENTERED", body={"values": [drivers]}).execute()
    except HttpError as err:
        print(err)
def add_early_driver(driver):
    try:
        sheet = get_sheet()
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B5:M5").execute().get('values', [])[0]
        drivers = set(drivers)
        drivers.add(driver)
        drivers = list(drivers)
        clear_cells(12, 1, 'drivers!B5:M5', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="drivers!B5:M5",
                             valueInputOption="USER_ENTERED", body={"values": [drivers]}).execute()
    except HttpError as err:
        print(err)
def remove_driver_going(driver):
    try:
        sheet = get_sheet()
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B1:M1").execute().get('values', [])[0]
        drivers = set(drivers)
        if driver in drivers:
            drivers.remove(driver)
        drivers = list(drivers)
        clear_cells(12, 1, 'drivers!B1:M1', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="drivers!B1:M1",
                             valueInputOption="USER_ENTERED", body={"values": [drivers]}).execute()
    except HttpError as err:
        print(err)
def remove_driver_returning(driver):
    try:
        sheet = get_sheet()
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B3:M3").execute().get('values', [])[0]
        drivers = set(drivers)
        if driver in drivers:
            drivers.remove(driver)
        drivers = list(drivers)
        clear_cells(12, 1, 'drivers!B3:M3', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="drivers!B3:M3",
                             valueInputOption="USER_ENTERED", body={"values": [drivers]}).execute()
    except HttpError as err:
        print(err)
def remove_early_driver(driver):
    try:
        sheet = get_sheet()
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B5:M5").execute().get('values', [])[0]
        drivers = set(drivers)
        if driver in drivers:
            drivers.remove(driver)
        drivers = list(drivers)
        clear_cells(12, 1, 'drivers!B5:M5', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="drivers!B5:M5",
                             valueInputOption="USER_ENTERED", body={"values": [drivers]}).execute()
    except HttpError as err:
        print(err)


def assign_rides_back():
    try:
        update_signups()
        sheet = get_sheet()
        areas = get_areas()

        #assign people to cars
        #drivers = ['heidi', 'jessica', 'elliot', 'alex park', 'joel', 'erik', 'camryn']
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B1:M1").execute().get('values', [])[0]

        #account for too many sign ups for # of drivers
        if 4*len(drivers) < sum([len(v) for _, v in areas.items()]):
            return 'not enough cars to take everyone'
        
        #for now, might change later to load from the google sheets or something
        prio = dict()
        prio['heidi'] = ['mesa', 'middle earth', 'plaza', 'vdc/vdcn', 'offcampus']
        prio['jessica'] = ['plaza', 'vdc/vdcn', 'middle earth', 'mesa', 'offcampus']
        prio['elliot'] = ['middle earth', 'plaza', 'vdc/vdcn', 'mesa', 'offcampus']
        prio['alex park'] = ['offcampus', 'mesa', 'middle earth', 'plaza', 'vdc/vdcn']
        prio['joel'] = ['offcampus', 'mesa', 'middle earth', 'plaza', 'vdc/vdcn']
        prio['erik'] = ['offcampus', 'mesa', 'middle earth', 'plaza', 'vdc/vdcn']
        prio['camryn'] = ['offcampus', 'mesa', 'middle earth', 'plaza', 'vdc/vdcn']
        
        #go from driver to driver, taking all people of their first prio
        #repeat for second prio until cars are full

        #^^ this thing does not work well lol
        #maybe doing something like assigning a weight where prio is a sum (min desired) and # of different places 
        #per car is a multiplier, and we're trying to minimize the total sum of all the cars

        cars = defaultdict(list)
        prio_index = 0
        people_num = sum([len(v) for k, v in areas.items()])
        while people_num > 0:
            for d in drivers:
                if len(cars[d]) < 4:
                    while len(areas[prio[d][prio_index]])>0 and len(cars[d])<4:
                        cars[d].append(areas[prio[d][prio_index]][0][0])
                        areas[prio[d][prio_index]].pop(0)
                        people_num -= 1

            prio_index += 1

        # for k, v in cars.items():
        #     print(k)
        #     print(v)
        #     print()

        #formatting for google sheets
        output = [[]]

        for d in drivers:
            output[0].append(d)

        while True:
            something = False
            temp = []

            for d in output[0]:
                if len(cars[d]) > 0:
                    temp.append(cars[d][0])
                    cars[d].pop(0)
                    something = True
                else:
                    temp.append('')

            output.append(temp)

            if not something:
                break

        # print(output)

        clear_cells(10, 6, "rides!B11:K16", sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="rides!B11:K16",
                             valueInputOption="USER_ENTERED", body={"values": output}).execute()

        return 'updated spreadsheet on the rides tab for RETURNING rides'
    
    except HttpError as err:
        print(err)


def get_areas():
    try:
        update_signups()
        sheet = get_sheet()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Current!B2:H100").execute()
        values = result.get('values', [])

        #get values
        early = []  #all areas just grouped in here
        areas = defaultdict(list)  #mesa, middle, plaza, vdc/vdcn, puerta, off campus
        for row in values:
            #account for deletion of duplicates
            if len(row)==0:
                print('did it')
                continue
            person = None
            if len(row[0])>5:
                index = row[0].rfind(' ')
                if index==-1:
                    person = row[0]
                else:
                    person = row[0][:index]
            else:
                person = row[0]
            #divide into early and fellowship
            if row[5]=='NO':
                early.append((person, row[4]))
            else:
                if 'mesa' in row[4].lower():
                    areas['mesa'].append((person, row[4]))
                elif 'brandy' in row[4].lower() or 'middle' in row[4].lower():
                    areas['middle earth'].append((person, row[4]))
                elif 'plaza' in row[4].lower():
                    areas['plaza'].append((person, row[4]))
                elif 'vdc' in row[4].lower():
                    areas['vdc/vdcn'].append((person, row[4]))
                elif 'puerta' in row[4].lower():
                    areas['vdc/vdcn'].append((person, row[4]))
                else:
                    areas['offcampus'].append((person, row[4]))

        # for k, v in areas.items():
        #     print(k, len(v))
        #     print(v)
        #     print()

        # return 'omegalul'

        #translate dict to list of lists for google sheets api
        output = []
        output.append([])
        for k, v in sorted(areas.items(), key=lambda x:x[0]):
            if k=='offcampus':
                continue
            output[0].append(f'{k}-({len(v)})')
        output[0].append(f"offcampus-({len(areas['offcampus'])})")

        index = 0
        while True:
            temp = []
            empty = True
            for k in output[0]:
                if index>=len(areas[k.split('-')[0]]):
                    temp.append('')
                else:
                    a = areas[k.split('-')[0]][index]
                    temp.append(f'{a[0]}')
                    empty = False
            output.append(temp)
            index += 1
            if empty:
                break

        #account for early people
        output[0].append(f'early-({len(early)})')
        for i in range(1, 1+len(early)):
            output[i].append(early[i-1][0])

        
        #formatting
        for i in range(len(output[0])):
            output[0][i] = output[0][i].replace('-', ' ')

        #update sheets where people need to be dropped off
        clear_cells(6, 11, 'rides!B17:G27', sheet)
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="rides!B17:G27",
                             valueInputOption="USER_ENTERED", body={"values": output}).execute()
        
        return areas
    
    except HttpError as err:
        print(err)


def assign_rides_going():
    try:
        update_signups()
        sheet = get_sheet()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Current!B2:H100").execute()
        values = result.get('values', [])

        #get values in the sheet
        people = []
        for row in values:
            #account for deletion of duplicates
            if len(row)==0:
                print('did it')
                continue
            if len(row[0])>5:
                index = row[0].rfind(' ')
                if index==-1:
                    people.append(row[0])
                else:
                    people.append(row[0][:index])
            else:
                people.append(row[0])

        #clear cells in previous ride assignement
        clear_cells(10, 5, "rides!B2:K6", sheet)

        #make the list of lists for the rides sheet (all random)
        # drivers = ['heidi', 'jessica', 'elliot', 'joel', 'erik', 'camryn', 'alex park']
        drivers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="drivers!B3:M3").execute().get('values', [])[0]

        #account for too many sign ups for # of drivers
        if 4*len(drivers) < len(people):
            return 'not enough cars to take everyone'

        output = [[]]
        for d in drivers:
            output[0].append(d)
        
        while len(people) > 0:
            temp = []
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

        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="rides!B2:K6",
                             valueInputOption="USER_ENTERED", body={"values": output}).execute()


        return 'updated spreadsheet on the rides tab for GOING rides'

    except HttpError as err:
        print(err)


def announce_rides_going():
    return announce_rides_helper("GOING to", "B2:K6")


def announce_rides_back():
    return announce_rides_helper("RETURNING from", "B11:K15")


def announce_rides_helper(header, custom_range):
    try:
        sheet = get_sheet()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"rides!{custom_range}").execute()
        values = result.get('values', [])

        #change from row to cols
        cars = []
        first = True

        for row in values:
            if first:
                first = False
                for d in row:
                    cars.append([d])
            else:
                for i in range(len(row)):
                    cars[i].append(row[i])

        # print(cars)

        output = f'> # __**Rides for {header} Gethsemane !**__\n'
        for c in cars:
            temp = ''
            for i in range(len(c)):
                if i==0:
                    temp += f'**{c[i]}**  -  '
                else:
                    temp += f'{c[i]},  '
            temp = temp[:-3]
            output += f'> {temp}\n'

        return output

    except HttpError as err:
        print(err)


def update_signups():
    try:
        sheet = get_sheet()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Current!A2:J100").execute()
        values = result.get('values', [])

        unique = dict()
        for row in values:
            if len(row) < 2:
                continue
            unique[row[1].lower()] = row
        
        clear_cells(10, 99, "Current!A2:J100", sheet)

        output = sorted([v for k, v in unique.items()], key=lambda x:x[0])
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Current!A2:J100",
                             valueInputOption="USER_ENTERED", body={"values": output}).execute()


    except HttpError as err:
        print(err)

    return 'Updated signups list to remove duplicates/blank lines !'


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

        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"{custom_range}",
                             valueInputOption="USER_ENTERED", body={"values": empty}).execute()
       
    except HttpError as err:
        print(err)


# print(get_areas())
# assign_rides_back()
# assign_rides_going()
# announce_rides_going()
# update_signups()