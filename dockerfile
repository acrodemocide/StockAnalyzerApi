# Backend Dockerfile
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY backend/ ./

# Optional: If you have a default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "StockAnalyzer.wsgi:application"]
