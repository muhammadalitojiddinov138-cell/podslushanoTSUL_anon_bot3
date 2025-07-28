# Используем официальный Python образ
FROM python:3.10-slim

# Устанавливаем зависимости для сборки (если нужны)
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Указываем порт для Render
ENV PORT=10000

# Запускаем бота
CMD ["python", "bot.py"]
