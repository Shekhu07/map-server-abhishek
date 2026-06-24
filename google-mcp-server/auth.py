import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes required by the application
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/gmail.compose'
]

def get_credentials():
    """
    Retrieves the Google OAuth 2.0 credentials.
    Loads from token.json if it exists and is valid.
    Otherwise, runs the local authorization flow using credentials.json
    and saves the token to token.json.
    """
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f"Error loading token.json: {e}. Re-authenticating...")
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}. Re-authenticating...")
                creds = None
        
        # If refreshing failed or is not possible, run the flow
        if not creds:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json not found. Please download your OAuth 2.0 client ID "
                    "credentials from the Google Cloud Console and place it in the root folder."
                )
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            # Use port=0 to find any available open port
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
            
    return creds
