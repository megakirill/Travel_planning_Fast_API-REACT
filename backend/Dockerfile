FROM python:3.9-slim

WORKDIR .

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN uvicorn app:app --reload
