import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from auth import get_credentials

def create_email_draft(to: str, subject: str, body: str):
    """
    Creates an email draft in the user's Gmail account.
    
    Args:
        to (str): Recipient's email address.
        subject (str): Subject of the email.
        body (str): Content body of the email.
    """
    # Retrieve authenticated credentials
    creds = get_credentials()
    
    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    
    # Construct the raw email message structure
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['Subject'] = subject
    
    # Base64 urlsafe encode the message as bytes, then decode to string
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    # Structure the draft body parameter
    draft_body = {
        'message': {
            'raw': raw_message
        }
    }
    
    # Create the email draft using Gmail API
    draft = service.users().drafts().create(userId='me', body=draft_body).execute()
    
    return draft
