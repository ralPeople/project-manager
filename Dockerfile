# Используем минимальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /project-manager

# Копируем зависимости
COPY req.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r req.txt

# Копируем всё (кроме venv и instance/DB.db, если хочешь сохранить локальную БД)
COPY . .

# Устанавливаем переменные среды
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Открываем порт Flask
EXPOSE 5000

# Запуск Flask
CMD ["flask", "run"]