#!/bin/bash

# Export variables from .env file to environment variables
export $(cat /usr/share/logstash/pipeline/.env | xargs)

# Substitute variables in create-topic.sh and logstash.conf
envsubst < /usr/share/logstash/pipeline/logstash.template.conf > /usr/share/logstash/pipeline/logstash.conf

# Ensure the substituted files have the correct permissions
chown root:root /usr/share/logstash/pipeline/logstash.conf

# Execute the Python script
exec logstash -f /usr/share/logstash/pipeline/logstash.conf