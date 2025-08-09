# ===== Stage 1: Install dependencies =====
FROM python:3.12-slim AS builder

# Install system dependencies required for asyncpg and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies into a separate directory
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# ===== Stage 2: Runtime image =====
FROM python:3.12-slim

# Install only runtime dependencies for PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy the entire application source code
COPY . .

# Build-time arguments (default values, can be overridden via --build-arg)
ARG POSTGRES_PORT=5432
ARG POSTGRES_HOST=localhost
ARG POSTGRES_DRIVER=postgresql+asyncpg
ARG POSTGRES_DATABASE=load_testing_metrics_db
ARG POSTGRES_USERNAME=load_testing_metrics_user
ARG POSTGRES_PASSWORD=load_testing_metrics_password
ARG KIBANA_URL=""
ARG GRAFANA_URL=""
ARG KUBERNETES_URL=""

# Set environment variables in the runtime container
ENV POSTGRES_PORT=${POSTGRES_PORT}
ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_DRIVER=${POSTGRES_DRIVER}
ENV POSTGRES_DATABASE=${POSTGRES_DATABASE}
ENV POSTGRES_USERNAME=${POSTGRES_USERNAME}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV KIBANA_URL=${KIBANA_URL}
ENV GRAFANA_URL=${GRAFANA_URL}
ENV KUBERNETES_URL=${KUBERNETES_URL}
ENV PYTHONUNBUFFERED=1


# Expose the port for uvicorn
EXPOSE 8000

# Run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
