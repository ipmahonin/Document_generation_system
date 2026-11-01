FROM python:3.11-slim

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

# Копируем код
COPY . .

# Команда по умолчанию
ENTRYPOINT ["/entrypoint.sh"]