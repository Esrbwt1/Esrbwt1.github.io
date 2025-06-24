# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /usr/src/app

# Install necessary libraries within the container
RUN pip install firebase-admin

# Copy our new persistent agent code into the container
COPY ./agents/agent_v4_persistent.py ./agent.py

# Label the container
LABEL project="Project Chrysalis"
LABEL version="4.0-persistent"

# The command to run when the container starts
CMD [ "python", "-u", "./agent.py" ]