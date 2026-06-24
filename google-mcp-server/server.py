import asyncio
import os
from fastapi import FastAPI, HTTPException, status, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(
    title="Google Workspace MCP Server",
    description="MCP-style API server integrating Google Docs and Gmail with API Key authentication."
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    expected_api_key = os.environ.get("API_KEY")
    if not expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API_KEY environment variable is not configured on the server."
        )
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

class DocPayload(BaseModel):
    doc_id: str
    content: str

class EmailPayload(BaseModel):
    to: str
    subject: str
    body: str

@app.get("/")
def read_root():
    return {"message": "Google MCP Server is running. Use POST /append_to_doc and POST /create_email_draft."}

@app.post("/append_to_doc")
async def handle_append_to_doc(payload: DocPayload, api_key: str = Depends(verify_api_key)):
    
    try:
        # Execute Docs action in a thread to keep FastAPI responsive
        result = await asyncio.to_thread(
            append_to_doc, payload.doc_id, payload.content
        )
        return {
            "status": "success",
            "message": "Content successfully appended to document.",
            "documentId": payload.doc_id,
            "response": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute Google Docs update: {str(e)}"
        )

@app.post("/create_email_draft")
async def handle_create_email_draft(payload: EmailPayload, api_key: str = Depends(verify_api_key)):
    
    try:
        # Execute Gmail action in a thread
        result = await asyncio.to_thread(
            create_email_draft, payload.to, payload.subject, payload.body
        )
        return {
            "status": "success",
            "message": "Gmail draft successfully created.",
            "response": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Gmail draft: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Start uvicorn server locally
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
