# --- Builder Stage ---
FROM python:3.13-slim AS builder

WORKDIR /app

# This section is critical for psycopg2 to build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt # <--- This is the line that's failing

# --- Final Stage ---
FROM python:3.13-slim

# This section is critical for psycopg2 to run (libpq.so.5) and Pillow runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    zlib1g \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/

# Explicitly install gunicorn in the FINAL stage
RUN pip install gunicorn

WORKDIR /app
COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
