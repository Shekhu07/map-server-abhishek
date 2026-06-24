from googleapiclient.discovery import build
from auth import get_credentials

def append_to_doc(doc_id: str, content: str):
    """
    Appends text content to the end of the specified Google Document.
    
    Args:
        doc_id (str): The Google Doc ID.
        content (str): The text content to append.
    """
    # Retrieve authenticated credentials
    creds = get_credentials()
    
    # Build the Google Docs service
    service = build('docs', 'v1', credentials=creds)
    
    # Retrieve the document to find the current end index
    doc = service.documents().get(documentId=doc_id).execute()
    
    # The document body content contains structural elements.
    # The last element's endIndex (minus 1) represents the position right before the document end.
    body_content = doc.get('body', {}).get('content', [])
    if body_content:
        end_index = body_content[-1].get('endIndex') - 1
    else:
        end_index = 1
        
    # Safeguard to prevent invalid indices
    if end_index < 1:
        end_index = 1
        
    # Construct the insert request
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index
                },
                'text': content
            }
        }
    ]
    
    # Execute the batch update to append the text
    response = service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    
    return response
