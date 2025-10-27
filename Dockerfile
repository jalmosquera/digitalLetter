FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.production

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

# Run migrations, collectstatic, create superuser, and start gunicorn
CMD ["sh", "-c", "echo 'Starting deployment...' && python manage.py migrate && echo 'Migrations complete. Running collectstatic...' && python manage.py collectstatic --noinput && echo 'Collectstatic complete. Creating superuser...' && python manage.py create_default_superuser && echo 'Superuser setup complete. Starting gunicorn...' && gunicorn core.wsgi --bind 0.0.0.0:8000 --log-file - --access-logfile - --error-logfile - --workers 2"]
