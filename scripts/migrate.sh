#!/bin/bash

docker exec -it fastapi_backend sh -c "PYTHONPATH=. alembic upgrade head"