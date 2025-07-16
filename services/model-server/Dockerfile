# Use a minimal Python 3.11 base image to keep the image size small
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file first (leveraging Docker layer caching)
COPY requirements.txt .

# Install Python dependencies without caching wheels (to reduce image size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code into the container
COPY . .

# Run the FastAPI app using Gunicorn with Uvicorn workers (for async support)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--capture-output", "--log-level", "debug"]
