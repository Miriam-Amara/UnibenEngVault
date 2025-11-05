# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# --- START FIX: Install libmagic system dependency ---
# libmagic1 provides the shared library for runtime use
# libmagic-dev provides the headers needed for compiling the python-magic wrapper (best to include)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 libmagic-dev && \
    rm -rf /var/lib/apt/lists/*
# --- END FIX ---


# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- FIX 2: COPY all application source code from the root into the working directory ---
COPY . .

# Expose the port the app will run on (This is fine, but Render uses the $PORT env var)
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "api.v1.app:app"]