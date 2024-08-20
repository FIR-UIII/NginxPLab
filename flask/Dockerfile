# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install ping, curl, and wget
RUN apt-get update && \
    apt-get install -y iputils-ping curl wget && \
    rm -rf /var/lib/apt/lists/*

# устанавливаем зависимости
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# копируем содержимое в каталог контерйнера
COPY . /app

# открываем порт для контента
EXPOSE 5000