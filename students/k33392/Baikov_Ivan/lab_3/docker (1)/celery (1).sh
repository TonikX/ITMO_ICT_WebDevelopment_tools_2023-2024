#!/bin/bash

echo "Starting Celery worker..."
celery -A worker:worker worker -l INFO --pool=prefork