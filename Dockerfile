# Укажите базовый образ
FROM python:3.9

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл requirements.txt и установите зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все остальные файлы в рабочую директорию
COPY . .

# Выполните миграции базы данных
EXPOSE 8000

# Укажите команду для запуска Django сервера
CMD ["sh", "-c", "python manage.py makemigrations", "python manage.py migrate", "python manage.py runserver 0.0.0.0:8000"]
