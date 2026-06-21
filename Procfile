web: cd backend && ../.venv/bin/python manage.py migrate --noinput && ../.venv/bin/gunicorn inventory_system.wsgi:application --bind 0.0.0.0:$PORT
