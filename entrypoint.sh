#!/bin/sh

echo "Waiting for Postgres..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Applying database migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn src.main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload