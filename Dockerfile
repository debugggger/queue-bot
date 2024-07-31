# Используем базовый образ с установленным Python
FROM python:3.10-slim

# Устанавливаем рабочий каталог внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочий каталог контейнера, исключая .env
COPY . .

# Указываем команду для запуска вашего бота
CMD ["python", "Src/queueBot.py"]