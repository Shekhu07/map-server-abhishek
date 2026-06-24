# Railway Deployment Plan for Google Workspace MCP Server

This document outlines the steps to deploy this MCP Server to [Railway](https://railway.app). 

> [!NOTE]
> **Codebase Modifications (Completed)**
> All necessary codebase modifications for cloud deployment have been implemented:
> - **API Key Authentication**: Terminal `input()` prompts in `server.py` have been replaced with a secure `X-API-Key` header check.
> - **Start Script**: `start.sh` was created to securely load your Base64 encoded credentials and start `uvicorn`.
> - **Railway Config**: `railway.json` was added to automatically tell Railway how to build and start your application.
> - **Dependencies**: `requirements.txt` was moved to the root folder for automatic detection.
> - **Git Ignore**: `.gitignore` was configured to prevent `credentials.json` and `token.json` from being committed.

## 1. Prepare GitHub Repository

Since the codebase is ready, you need to push it to a GitHub repository:

1. Open your terminal in the `MCP Server` directory.
2. Initialize and push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with Railway deployment configuration"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

## 2. Encode Secrets Locally

Your Google credentials must be passed to Railway securely as environment variables. Run the following commands in your local terminal to get the base64 versions:

```bash
cat credentials.json | base64
```
*(Copy the output string)*

```bash
cat token.json | base64
```
*(Copy the output string)*

## 3. Deploy on Railway

1. Go to your [Railway dashboard](https://railway.app/dashboard) and click **New Project** -> **Deploy from GitHub repo**.
2. Select your newly created MCP Server repository.
3. Railway will start building automatically using the settings in `railway.json`. It might fail the very first time because the environment variables aren't set yet.
4. Go to your new Railway service's **Variables** tab and add the following:
   - `GOOGLE_CREDENTIALS_BASE64`: *(paste the base64 string for credentials.json)*
   - `GOOGLE_TOKEN_BASE64`: *(paste the base64 string for token.json)*
   - `API_KEY`: *(create a strong secret password/key. You will use this in your HTTP headers to access the server)*
5. Railway will redeploy automatically with the variables applied.

## 4. Expose the Service

1. In the Railway **Settings** tab, go to the **Networking** section.
2. Click **Generate Domain** to get a public URL for your MCP server.

## 5. Post-Deployment Verification

1. Once deployed, visit `https://<your-railway-domain>/` in your browser. You should see the root message.
2. Test the `/append_to_doc` or `/create_email_draft` endpoints using an HTTP client (like cURL or Postman). 
   - **Crucial**: You must pass the header `X-API-Key: <your_secret_key>` in your request, otherwise you will receive a 403 Forbidden error!
