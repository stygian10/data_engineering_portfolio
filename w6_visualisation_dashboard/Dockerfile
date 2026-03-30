# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the source code
COPY . .

# Expose port 8050 for Dash
EXPOSE 8050

# Run the dashboard
CMD ["python", "src/app.py"]