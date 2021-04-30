FROM python:alpine3.7

COPY . /app
WORKDIR /app

RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev
RUN apk add curl

RUN python3 -m pip install pip==21.0.1 --disable-pip-version-check
RUN python3 -m pip install -r requirements.txt --disable-pip-version-check

RUN chmod +x run_tests.sh

EXPOSE 80

CMD uvicorn run:app --reload --host 0.0.0.0
