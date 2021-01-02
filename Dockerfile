FROM python:3
ENV pythonbuffered=1
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
