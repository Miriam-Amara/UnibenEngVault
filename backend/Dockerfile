# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# --- FIX 1: COPY requirements.txt from root into the working directory ---
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- FIX 2: COPY all application source code from the root into the working directory ---
COPY . .

# Expose the port the app will run on (This is fine, but Render uses the $PORT env var)
EXPOSE 8000

# Run Gunicorn with 2 workers
# --- FIX 3: Update the command to match the new root location ---
# The entry point is now simply 'api.v1.app:app' if the code is in /app/api/v1/app.py
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "api.v1.app:app"]