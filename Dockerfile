# Base Image
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev libffi-dev

# Copy application code
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app/src

# Expose application port
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]