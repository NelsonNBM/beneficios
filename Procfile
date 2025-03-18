release: python manage.py collectstatic --noinput
web: gunicorn maquina.wsgi --bind 0.0.0.0:$PORT

