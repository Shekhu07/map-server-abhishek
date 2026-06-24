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


def find_section_by_anchor(doc_id: str, anchor: str) -> bool:
    """
    Searches the specified Google Document for an exact text match of the anchor string.
    
    Args:
        doc_id (str): The Google Doc ID.
        anchor (str): The text string to search for.
        
    Returns:
        bool: True if the anchor text is found in the document, False otherwise.
    """
    # Retrieve authenticated credentials
    creds = get_credentials()
    
    # Build the Google Docs service
    service = build('docs', 'v1', credentials=creds)
    
    # Retrieve the document content
    doc = service.documents().get(documentId=doc_id).execute()
    
    # Extract all text elements from the document body
    body_content = doc.get('body', {}).get('content', [])
    
    # Simple search: look through all text elements for the anchor string
    for element in body_content:
        if 'paragraph' in element:
            for pe in element['paragraph'].get('elements', []):
                if 'textRun' in pe:
                    text = pe['textRun'].get('content', '')
                    if anchor in text:
                        return True
                        
    return False

