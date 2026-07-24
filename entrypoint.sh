#!/bin/sh

set -e

echo "Applying migrations..."

alembic upgrade head

echo "Adding initial data..."

python -m app.scripts.seed

echo "Starting FastAPI..."

uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload