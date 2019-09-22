# Use an official Python runtime as a parent image
FROM python:3.7-slim-stretch

# Get and run the Packages
RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# COPY (is prefered over ADD unless tar) the file to container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# had to remove --upgrade because:
# Killed
# The command '/bin/sh -c pip install --upgrade -r requirements.txt' returned a non-zero code: 137
RUN pip install -r requirements.txt

# Then copy the app directory
COPY . .

# Run the app
RUN python server.py

# Expose the app to the world
EXPOSE 8000


# Serve the app with uvicorn when container launches
CMD ["python", "server.py", "serve"]