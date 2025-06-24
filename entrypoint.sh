#!/bin/sh
set -e
PEM_FILE_PATH="/app/mr-stark-logs.pem"

if [ -n "$RSA_PRIVATE_KEY_B64" ]; then
  echo "RSA_PRIVATE_KEY_B64 environment variable found. Decoding and creating $PEM_FILE_PATH..."
  echo "$RSA_PRIVATE_KEY_B64" | base64 -d > "$PEM_FILE_PATH"
  chmod 600 "$PEM_FILE_PATH"
  echo "$PEM_FILE_PATH created successfully."
else
  echo "Warning: RSA_PRIVATE_KEY_B64 environment variable not set. The file $PEM_FILE_PATH will not be created."
  echo "The bot might not function correctly if this key is required for initialization."
fi

exec "$@"