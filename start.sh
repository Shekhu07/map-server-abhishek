#!/bin/bash

# Write the raw JSON environment variables to files
if [ -n "$GOOGLE_CREDENTIALS_JSON" ]; then
    echo "$GOOGLE_CREDENTIALS_JSON" > credentials.json
    echo "credentials.json has been created from environment variables."
fi

if [ -n "$GOOGLE_TOKEN_JSON" ]; then
    echo "$GOOGLE_TOKEN_JSON" > token.json
    echo "token.json has been created from environment variables."
fi

export PYTHONPATH=./google-mcp-server
uvicorn google-mcp-server.server:app --host 0.0.0.0 --port ${PORT:-8000}
