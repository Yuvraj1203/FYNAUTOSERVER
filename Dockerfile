# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bullseye

# Set environment variables using the modern format
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /src/fynautoserver

# Install system dependencies for wkhtmltopdf
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxrender1 \
    libfontconfig1 \
    libqt5webkit5 \
    wkhtmltopdf \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install poetry globally
RUN pip install --no-cache-dir poetry

# Copy project files to the container
COPY . .

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi

RUN poetry install

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "dev"]
