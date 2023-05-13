import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']
MISCELLANEOUS_LIST_ID = ""
COURSEWORK_LIST_ID = ""

def getListFromJson(json):
     
     json = json['items']
     my_list = []
     for dict in json:
        my_list.append(dict['title'])
    
     return my_list


def googletasks(misc, coursework):

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('tasks', 'v1', credentials=creds)

        # Call the TasksAPI
        google_misc = service.tasks().list(tasklist=MISCELLANEOUS_LIST_ID).execute()
        google_coursework = service.tasks().list(tasklist=COURSEWORK_LIST_ID).execute()

        google_misc_list = getListFromJson(google_misc)
        google_coursework_list = getListFromJson(google_coursework)


        for json_body in misc: 
            if json_body['title'] in google_misc_list:
                continue 
            service.tasks().insert(tasklist=MISCELLANEOUS_LIST_ID, body=json_body).execute()
        
        for json_body in coursework:
            if json_body['title'] in google_coursework_list:
                continue
            service.tasks().insert(tasklist=COURSEWORK_LIST_ID, body=json_body).execute()

    except HttpError as err:
        print(err)


