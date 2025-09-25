# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Create a non-root user first
RUN useradd --create-home --shell /bin/bash app

# Copy dependency files and change ownership
COPY pyproject.toml uv.lock ./
RUN chown -R app:app /app

# Switch to non-root user for dependency installation
USER app

# Install dependencies using uv (as non-root user)
RUN uv sync --frozen

# Copy source code and change ownership
COPY --chown=app:app . .

# Expose port (if needed for future web interface)
EXPOSE 8000

# Default command
CMD ["uv", "run", "python", "main.py"]
