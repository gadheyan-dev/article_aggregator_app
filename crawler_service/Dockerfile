FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

COPY . /app/

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8004

CMD ["gunicorn", "--bind", "0.0.0.0:8004", "--reload", "crawler_service.wsgi:application", "--access-logfile", "-"]