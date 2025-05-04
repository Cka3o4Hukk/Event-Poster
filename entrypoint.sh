#!/bin/sh

python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
python manage.py collectstatic --noinput
exec gunicorn events_app.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 