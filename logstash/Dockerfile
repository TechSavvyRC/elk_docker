# Use Logstash base image
FROM docker.elastic.co/logstash/logstash:8.15.0

# Set working directory
WORKDIR /usr/share/logstash/pipeline

# Switch to root user to install packages
USER root

# Install requied packages
RUN apt-get update && apt-get install -y gettext-base vim net-tools inetutils-ping netcat-traditional

# Copy scripts and configuration templates
COPY .env /usr/share/logstash/pipeline
COPY logstash.template.conf /usr/share/logstash/pipeline
COPY entrypoint.sh /usr/share/logstash/pipeline

# Give execution rights to the script
RUN chmod +x /usr/share/logstash/pipeline/entrypoint.sh

# Substitute environment variables in the Python script
ENTRYPOINT ["/usr/share/logstash/pipeline/entrypoint.sh"]
