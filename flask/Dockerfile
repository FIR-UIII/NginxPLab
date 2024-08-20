FROM python:3.8-slim

# устанавливаем рабочий каталог контейнера
WORKDIR /app

# устанавливаем зависимости
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# копируем содержимое в каталог контерйнера
COPY . /app

# открываем порт для контента
EXPOSE 5000