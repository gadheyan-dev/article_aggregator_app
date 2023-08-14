FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8010

CMD ["gunicorn", "--bind", "0.0.0.0:8010", "--reload", "tasks_service.wsgi:application", "--access-logfile", "-"]