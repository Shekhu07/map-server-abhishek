#!/bin/bash

# Decode the base64 environment variables and write them to JSON files
# This ensures that our secret tokens aren't hardcoded or checked into GitHub
if [ -n "$GOOGLE_CREDENTIALS_BASE64" ]; then
    echo "$GOOGLE_CREDENTIALS_BASE64" | base64 -d > credentials.json
    echo "credentials.json has been created from environment variables."
fi

if [ -n "$GOOGLE_TOKEN_BASE64" ]; then
    echo "$GOOGLE_TOKEN_BASE64" | base64 -d > token.json
    echo "token.json has been created from environment variables."
fi

# We assume that the working directory needs to be google-mcp-server
# to run the server if it's not already, or we can just run it from the root.
# Given the code expects credentials to be in the CWD, we run uvicorn from the root
# where credentials.json/token.json are created.
export PYTHONPATH=./google-mcp-server
uvicorn google-mcp-server.server:app --host 0.0.0.0 --port ${PORT:-8000}
