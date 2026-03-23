FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY static/ ./static/

# Expose application port
EXPOSE 8080

# Run the FastAPI application
CMD ["python", "main.py"]
