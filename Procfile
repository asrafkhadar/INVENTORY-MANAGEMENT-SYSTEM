web: .venv/bin/python backend/manage.py migrate --noinput && .venv/bin/gunicorn backend.inventory_system.wsgi:application --bind 0.0.0.0:$PORT
