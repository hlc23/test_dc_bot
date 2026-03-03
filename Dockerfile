# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory to /app
WORKDIR /app

# Copy the used directory and contents into the container at /app
COPY ./cogs /app/cogs
COPY ./core /app/core
# COPY ./data /app/data # mount data volume instead of copying
COPY ./utils /app/utils
COPY ./main.py /app/
COPY ./requirements.txt /app/

# Install build dependencies required for packages that need C compilation (e.g. aiohttp)
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Run app.py when the container launches
CMD ["python", "main.py"]
