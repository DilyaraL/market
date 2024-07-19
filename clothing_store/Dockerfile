FROM python:3.9-slim

# Устанавливаем зависимости для работы с PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY .. /app

# Устанавливаем зависимости проекта
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "clothing_store.wsgi:application"]