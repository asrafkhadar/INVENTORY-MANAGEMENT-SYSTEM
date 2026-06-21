web: python3 backend/manage.py migrate --noinput && gunicorn backend.inventory_system.wsgi:application --bind 0.0.0.0:$PORT
