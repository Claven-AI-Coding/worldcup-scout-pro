#!/bin/bash
set -e

echo "=== World Cup Scout Pro - Database Initialization ==="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h ${POSTGRES_HOST:-db} -U ${POSTGRES_USER:-scout} -q; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Run Alembic migrations
echo "Running database migrations..."
cd /app
alembic upgrade head
echo "Migrations complete!"

# Seed initial data
echo "Seeding initial data..."
python /app/../scripts/seed_data.py
echo "Seed data imported!"

echo "=== Database initialization complete ==="
