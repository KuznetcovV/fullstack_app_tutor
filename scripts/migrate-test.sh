#!/bin/bash

docker exec -it fastapi_backend sh -c "PYTHONPATH=. alembic -c alembic-test.ini upgrade head"