# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install requied packages
RUN apt-get update && apt-get install -y gettext-base vim net-tools inetutils-ping netcat-traditional

# Copy .env file and template Python script into the container
COPY .env /usr/src/app
COPY banking_app.template.py /usr/src/app
COPY entrypoint.sh /usr/src/app

# Give execution rights to the script
RUN chmod +x /usr/src/app/entrypoint.sh

# Substitute environment variables in the Python script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
