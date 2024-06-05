# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the used directory and contents into the container at /app
COPY ./cogs /app/cogs
COPY ./core /app/core
COPY ./data /app/data
COPY ./utils /app/utils
COPY ./main.py /app/
COPY ./requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Run app.py when the container launches
CMD ["python", "main.py"]
