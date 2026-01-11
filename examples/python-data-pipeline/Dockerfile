FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy sample data
COPY sample_events.csv . 2>/dev/null || true

# Environment variables
ENV DATABASE_URL="sqlite+aiosqlite:///pipeline.db"
ENV CSV_FILE="sample_events.csv"

# Run pipeline
CMD ["python", "-m", "src.main"]
