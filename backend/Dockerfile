# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt backend/requirements.txt

# Install Python dependencies
RUN pip install -r backend/requirements.txt

# Copy application code
COPY backend backend
COPY tradingagents tradingagents

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

ENV PYTHONPATH=/app
WORKDIR /app/backend

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
