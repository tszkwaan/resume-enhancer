FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make the script executable
RUN chmod +x scripts/extract_text.py

# Expose port (optional, for debugging)
EXPOSE 8000

# Default command
CMD ["python", "scripts/extract_text.py"]
