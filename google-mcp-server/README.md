# Google Workspace MCP-Style Server

A FastAPI-based Python server implementing Model Context Protocol (MCP) style endpoints for Google Docs and Gmail, with local terminal-based human-in-the-loop approvals.

## Features
- **FastAPI Backend**: Runs a local server with endpoints for Google Workspace operations.
- **OAuth 2.0 Auth**: Authenticates securely via Google OAuth 2.0 Desktop Application flow, caching local tokens to bypass re-login.
- **Google Docs Tool**: Appends text content to the end of a specified document.
- **Gmail Tool**: Generates email drafts with recipient, subject, and body parameters.
- **Human-in-the-loop Controls**: Prompts for `y/n` confirmation in the terminal console before performing any write action.

---

## 🛠️ Step 1: Google Cloud Setup

Before running the server, you need to configure a project in the Google Cloud Console to download `credentials.json`.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the APIs:
   - Go to **APIs & Services > Library**.
   - Search for and enable **Google Docs API**.
   - Search for and enable **Gmail API**.
4. Configure the **OAuth Consent Screen**:
   - Go to **APIs & Services > OAuth consent screen**.
   - Select user type **External** (unless you are part of a Google Workspace organization and want Internal).
   - Fill out the required App name, User support email, and Developer contact information.
   - Click **Save and Continue**.
   - Under **Scopes**, click **Add or Remove Scopes** and add:
     - `https://www.googleapis.com/auth/documents`
     - `https://www.googleapis.com/auth/gmail.compose`
   - Under **Test users**, add the email address of the Google Account you intend to authorize. *This is a mandatory step for apps in Testing mode.*
5. Create OAuth 2.0 Credentials:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials** and select **OAuth client ID**.
   - Select **Application type** as **Desktop app**.
   - Provide a name (e.g. `Google MCP Client`) and click **Create**.
   - In the credentials list, click the **Download JSON** icon (or copy client ID details) for your newly created OAuth Client.
   - Rename this downloaded file to `credentials.json` and place it in the `google-mcp-server/` root folder.

---

## 🚀 Step 2: Installation & Running

1. **Navigate to the server directory**:
   ```bash
   cd google-mcp-server
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI Server**:
   ```bash
   python server.py
   ```
   *Alternatively, start with uvicorn directly:*
   ```bash
   python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Authenticate (First-Time Only)**:
   - On the first run, or if `token.json` is missing or expired, a web browser tab will open automatically.
   - Log in using your Google Account (the one listed under **Test users**).
   - Since the app is unverified, click **Advanced** and then **Go to <App Name> (unsafe)**.
   - Grant the permissions for Google Docs and Gmail compose.
   - Once completed, the browser will display "The authentication flow has completed..." and a local `token.json` file will be generated in the root directory. Subsequent runs will skip this browser step.

---

## ⚡ Step 3: Usage & Endpoints

You can trigger the endpoints using `curl` or any API client (e.g., Postman).

### 1. Append to a Google Document

**Endpoint**: `POST http://127.0.0.1:8000/append_to_doc`

**Payload**:
```json
{
  "doc_id": "YOUR_GOOGLE_DOCUMENT_ID",
  "content": "\nThis text was appended by the Google MCP Server!"
}
```

**Example Curl**:
```bash
curl -X POST http://127.0.0.1:8000/append_to_doc \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "1234567890abcdefghijklmnopqrstuvwxyz",
    "content": "\nHello World from MCP!"
  }'
```

### 2. Create a Gmail Draft

**Endpoint**: `POST http://127.0.0.1:8000/create_email_draft`

**Payload**:
```json
{
  "to": "recipient@example.com",
  "subject": "Hello from Google MCP",
  "body": "This is a draft email body created via Google Workspace MCP server!"
}
```

**Example Curl**:
```bash
curl -X POST http://127.0.0.1:8000/create_email_draft \
  -H "Content-Type: application/json" \
  -d '{
    "to": "someone@example.com",
    "subject": "Automated Draft Subject",
    "body": "Hi,\n\nThis draft was generated from our Python MCP tool."
  }'
```

---

## 🛡️ Interactive Approvals

When a POST request is received, the server will log the action details to the terminal and pause execution:

```text
==================================================
⚠️  APPROVAL REQUESTED FOR: APPEND TO DOC
--------------------------------------------------
Payload details:
  • doc_id: 1234567890abcdefghijklmnopqrstuvwxyz
  • content: 
Hello World from MCP!
==================================================
Approve? (y/n): 
```

- Type **`y`** (and hit Enter) to proceed. The server will execute the API call and return `200 OK`.
- Type **`n`** (and hit Enter) to reject. The server will respond with `403 Forbidden` (`Action rejected by the server operator`).
