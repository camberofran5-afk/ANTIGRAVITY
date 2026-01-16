# Dockerfile for FastAPI Backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment defaults (can be overridden)
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose port
EXPOSE 8000

# Run commands
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
