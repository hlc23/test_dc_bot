FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD python3 main.py
