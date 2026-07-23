# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Expose Dash port
EXPOSE 8050

# Start the dashboard as a Python package
CMD ["python", "-m", "src.app"]