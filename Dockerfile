FROM python:3.11-slim

# Prevent Python from writing .pyc files and force stdout / stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory. The book uses /src but /app is more recommended
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first (for better caching). The book uses requirements.txt, but I am trying to ise the .toml file
COPY pyproject.toml ./

# Install python dependencies
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY test/ ./test/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -e ".[web]"

# Create entrypoints directory if needed
RUN mkdir -p /app/entrypoints

# Expose Flask port
EXPOSE 5000

# Set Flask environment variables. The book uses FLASK_DEBUG=1.
ENV FLASK_APP=batch_allocations.entrypoints.flask_app \
    FLASK_DEBUG=1 \
    PYTHONPATH=/app/src

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]


