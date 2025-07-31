FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost,127.0.0.1,*

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Copy project
COPY . .

# Create staticfiles and media directories and collect static files
RUN mkdir -p staticfiles && mkdir -p media && python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Change ownership of the app directory to the appuser
RUN chown -R appuser:appuser /app

# Ensure media directory has correct permissions
RUN chmod 755 /app/media

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "300", "--max-requests", "1000", "--max-requests-jitter", "100", "chronogallery.wsgi:application"] 