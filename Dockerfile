FROM python:3.8

# Run python in un-buffered mode. 
# It causes all output to stdout to be flushed immediately - for precise debugging of python app
ARG DB_ENGINE
ARG DB_HOST
ARG DB_NAME
ARG DB_PASS
ARG DB_USER
ARG DB_PORT

ENV DB_ENGINE ${DB_ENGINE}
ENV DB_HOST ${DB_HOST}
ENV DB_NAME ${DB_NAME}
ENV DB_PASS ${DB_PASS}
ENV DB_USER ${DB_USER}
ENV DB_PORT ${DB_PORT}
 
ENV PYTHONUNBUFFERED 1

ADD . /ece651-sns

WORKDIR /ece651-sns

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools

RUN pip install -r /ece651-sns/requirements.txt

RUN python manage.py wait_for_db

RUN ls sns/apps/product/migrations

RUN python manage.py makemigrations

RUN ls sns/apps/product/migrations

RUN python manage.py migrate

RUN python manage.py collectstatic

CMD gunicorn --bind 0.0.0.0:$PORT sns.wsgi