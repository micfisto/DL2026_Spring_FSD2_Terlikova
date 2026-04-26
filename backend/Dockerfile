FROM python:3.12-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy only requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
