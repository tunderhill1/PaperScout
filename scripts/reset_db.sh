#!/usr/bin/env bash

set -e  # exit on any error

echo "Stopping docker-compose services..."
docker-compose down

echo "Removing Postgres volume..."
VOLUME_NAME="paperscout_paperscout-db-data"

if docker volume ls | grep -q "$VOLUME_NAME"; then
  docker volume rm "$VOLUME_NAME"
  echo "✔ Deleted volume: $VOLUME_NAME"
else
  echo "⚠ Volume $VOLUME_NAME not found — nothing to delete."
fi

echo "Starting Docker services..."
docker-compose up -d

echo "Waiting for Postgres to be ready..."
sleep 3

echo "Running Alembic migrations..."
cd backend
alembic upgrade head
cd ..

echo "Database reset complete!"