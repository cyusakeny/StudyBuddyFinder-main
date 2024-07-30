from datetime import *
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from dotenv import load_dotenv
from googleapiclient.errors import HttpError


# Load environment variables from .env file
load_dotenv()

# Define Google API scopes
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
ALL_SCOPES = GMAIL_SCOPES + CALENDAR_SCOPES

def get_credentials():
    creds = None
    env_folder = os.getenv('ENV_FOLDER')
    creds_path = os.path.join(env_folder, 'token.json')
    credentials_path = os.path.join(env_folder, 'credentials.json')

    if os.path.exists(creds_path):
        creds = Credentials.from_authorized_user_file(creds_path, ALL_SCOPES)
        print("Found token.json, loading credentials...")
    else:
        print("token.json not found, initiating OAuth flow...")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Credentials expired, refreshing...")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, ALL_SCOPES)
            creds = flow.run_local_server(port=51912)
            print("OAuth flow completed, credentials obtained.")
        with open(creds_path, 'w') as token:
            token.write(creds.to_json())
            print("Credentials saved to token.json.")

    return creds

def get_gmail_service():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    print("Gmail service built successfully.")
    return service

def get_calendar_service():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    print("Calendar service built successfully.")
    return service

def send_email(user_email, subject, html_content):
    service = get_gmail_service()
    
    message = MIMEMultipart()
    message['to'] = user_email
    message['subject'] = subject
    message.attach(MIMEText(html_content, 'html'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw_message}
    
    try:
        message = service.users().messages().send(userId='me', body=message_body).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def create_calendar_event(summary, description, start_datetime, end_datetime, attendees_emails, group_id):
    service = get_calendar_service()
    
    api_key = os.getenv('API_KEY') # Get the API key from the config

    # Check if start_datetime and end_datetime are strings and convert them to the correct format
    if isinstance(start_datetime, str):
        start_datetime = datetime.strptime(start_datetime, '%d-%m-%Y %H:%M').isoformat()
    else:
        start_datetime = start_datetime.isoformat()
    
    if isinstance(end_datetime, str):
        end_datetime = datetime.strptime(end_datetime, '%d-%m-%Y %H:%M').isoformat()
    else:
        end_datetime = end_datetime.isoformat()
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'Africa/Harare',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'Africa/Harare',
        },
        'attendees': [{'email': email} for email in attendees_emails],
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string',  # Ideally, this should be a unique string for each request
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'status': {
                    'statusCode': 'success'
                }
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'extendedProperties': {
            'private': {
                'groupId': group_id
            }
        }
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1, key=api_key).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        meet_link = event['conferenceData']['entryPoints'][0]['uri']
        return event, meet_link
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None, None

def send_email_notification(attendees_emails,meet_link, summary):
    subject = f"New Event Created: {summary}"
    body = (
        f"Google Meet Link: <a href='{meet_link}'>Join Meeting</a>"
    )
    
    for email in attendees_emails:
        send_email(email, subject, body)