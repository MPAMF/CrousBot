FROM python:alpine3.17
RUN apk update \
    apk add \
    build-base \
    libpq \
    build-essential
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
COPY . .
CMD ["python", "main.py"]