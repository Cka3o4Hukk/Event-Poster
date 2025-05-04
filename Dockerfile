FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && pip install --no-cache-dir poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev --no-root

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get remove -y \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY events_app/ /app/events_app/
COPY events/     /app/events/
COPY manage.py   /app/
COPY entrypoint.sh /app/

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=events_app.settings \
    PYTHONPATH=/app

EXPOSE 8000

RUN adduser --disabled-password --no-create-home django && \
    mkdir -p /app/staticfiles && \
    chown -R django:django /app && \
    chmod +x /app/entrypoint.sh

USER django

CMD ["/app/entrypoint.sh"]