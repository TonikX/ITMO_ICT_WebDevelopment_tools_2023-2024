#!/bin/bash

echo "Starting Flower..."
celery -A worker:worker flower