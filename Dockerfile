FROM python:3.14-alpine

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаём рабочую директорию
WORKDIR /app

# Устанавливаем наркотические зависимости.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем проект.
COPY . .

# Открываем порт.
EXPOSE 8000