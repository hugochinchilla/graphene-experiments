FROM library/python:3.6.5-alpine
LABEL maintainer="Joan Font <jfont@habitissimo.com>"
LABEL maintainer="Hugo Chinchilla <hchinchilla@habitissimo.com>"

ARG BUILD_ENV=prod

WORKDIR /code/

RUN apk --update upgrade \
 && apk add postgresql-client \
	curl ca-certificates \
 &&	update-ca-certificates

ADD requirements*.txt /code/
RUN apk --update add --virtual build-dependencies \
    build-base \
    python3-dev \
    postgresql-dev \
 && pip3 install -U pip \
 && pip3 install -r requirements-${BUILD_ENV}.txt \
 && apk del build-dependencies \
 && rm -f /var/cache/apk/*

ADD . /code/

RUN SECRET_KEY=" " python3 manage.py collectstatic --noinput --no-color

EXPOSE 8080
CMD ["gunicorn", "foobar.wsgi", "-b", "0.0.0.0:8080", "--log-file=-"]
