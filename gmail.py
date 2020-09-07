"""Send an email using Gmail."""
import base64
from email.mime.text import MIMEText
import os.path
import pickle
from typing import Dict

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
ME = 'me'


def makedirs(path: str, isfile: bool = False):
    """
    Creates a directory given a path to either a directory or file.

    If a directory is provided, creates that directory. If a file is provided (i.e. isfile == True),
    creates the parent directory for that file.

    :param path: Path to a directory or file.
    :param isfile: Whether the provided path is a directory or file.
    """
    if isfile:
        path = os.path.dirname(path)
    if path != '':
        os.makedirs(path, exist_ok=True)


def create_message(to: str, subject: str, message_text: str) -> Dict[str, str]:
    """
    Creates a message for an email.

    :param to: Email address(es) of the receiver. Comma separated list for multiple emails.
    :param subject: Email subject line.
    :param message_text: Email message text.
    :return: A dictionary containing the base64url encoded email message object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = ME
    message['subject'] = subject

    email_message = {'raw': str(base64.urlsafe_b64encode(message.as_bytes()), 'utf-8')}

    return email_message


def send_message(service: Resource, message: Dict[str, str]) -> Dict[str, str]:
    """
    Sends an email message.

    :param service: The authenticated Gmail service object.
    :param message: A base64url encoded email message object.
    :return: The sent message.
    """
    try:
        message = service.users().messages().send(userId=ME, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')


def build_service(token_path: str = 'token.pickle',
                  credentials_path: str = 'credentials.json') -> Resource:
    """
    Builds a Gmail API service.

    :param token_path: Path to user token .pickle file. If it doesn't already exist,
                       it will be saved here.
    :param credentials_path: Path to credentials .json file.
    :return: Authenticated Gmail service.
    """
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    else:
        creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        makedirs(token_path, isfile=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)

    return service
