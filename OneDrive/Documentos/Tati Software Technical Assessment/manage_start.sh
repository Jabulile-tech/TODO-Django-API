#!/usr/bin/env bash
set -e

echo "Starting app startup script"

# Try migrating with retries to allow DB to become available
attempts=0
max_attempts=10
until python manage.py migrate --noinput; do
  attempts=$((attempts+1))
  if [ "$attempts" -ge "$max_attempts" ]; then
    echo "migrate failed after $attempts attempts"
    break
  fi
  echo "Waiting for DB (attempt $attempts/$max_attempts)..."
  sleep 5
done

echo "Collecting static files"
python manage.py collectstatic --noinput || true

# Create superuser non-interactively if env vars provided
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
  echo "Ensuring superuser $ADMIN_USERNAME exists"
  python manage.py shell <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$ADMIN_USERNAME"
email = "$ADMIN_EMAIL"
password = "$ADMIN_PASSWORD"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created')
else:
    print('Superuser already exists')
PY
fi

echo "Starting Gunicorn"
exec gunicorn todo_api.wsgi:application --bind 0.0.0.0:8000 --workers ${WEB_CONCURRENCY:-1} --timeout 60
