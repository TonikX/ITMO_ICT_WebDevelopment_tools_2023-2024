#!/bin/bash

# Run alembic migration
alembic revision --autogenerate -m "database initialised"
alembic upgrade head

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000