#!/bin/bash

# Export variables from .env file to environment variables
export $(cat /usr/src/app/.env | xargs)

# Substitute variables in cbanking_app.py and logstash.conf
envsubst < /usr/src/app/banking_app.template.py > /usr/src/app/banking_app.py

# Ensure the substituted files have the correct permissions
chmod +x /usr/src/app/banking_app.py

# Ensure the substituted file has the correct permissions
chmod +x banking_app.py

# Execute the Python script
exec python3 banking_app.py