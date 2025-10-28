# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for caching
COPY backend/requirements.txt ./backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.txt

# Copy the entire backend source code into /app/backend
COPY ./backend ./backend

# Expose the port the app will run on
EXPOSE 8000

# Run Gunicorn with 2 workers (safe for 1 CPU)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "backend.api.v1.app:app"]
