FROM python:3.12.0a7-alpine3.17

RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev openssl-dev libxml2-dev libxslt-dev zlib-dev libjpeg-turbo-dev libpng-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]