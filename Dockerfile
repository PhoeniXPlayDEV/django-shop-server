FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /web_django

WORKDIR /web_django
COPY requirements.txt /web_django/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD orders_app /web_django/
ADD orders_rest_app /web_django/
ADD shop_server /web_django/
ADD manage.py /web_django/
ADD pdm.lock /web_django/
ADD pyproject.toml /web_django/

#RUN python manage.py makemigrations
#RUN python manage.py migrate
