import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def get_google_api_service(client_secret_file, api_name, api_version, scopes, prefix=''):
    """
    Constructs and returns a Google API service instance.

    This function handles the OAuth 2.0 authentication flow, creating or loading
    a token file to manage credentials.

    Args:
        api_name (str): The name of the API (e.g., 'gmail').
        api_version (str): The version of the API (e.g., 'v1').
        scopes (list): A list of API scopes to request.
        client_secret_file (str, optional): The path to the credentials.json file.
                                          Defaults to 'credentials.json'.

    Returns:
        googleapiclient.discovery.Resource: A Google API service instance.
    """
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    creds = None
    working_dir = os.getcwd()
    token_dir = 'token_files'
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'

    # Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = json.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                raise FileNotFoundError(f"The file '{CLIENT_SECRET_FILE}' was not found. "
                                        "Please download it from the Google Cloud Console.")

            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None


if __name__ == '__main__':
    # Example usage for the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    client_secret_file = "client_secret.json"

    print("Constructing Gmail API service instance...")
    try:
        gmail_service = get_google_api_service(client_secret_file, 'gmail', 'v1', *SCOPES)
        print("Gmail API service instance created successfully.")

        # Example of how you would use the service:
        # results = gmail_service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])
        # print(labels)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")