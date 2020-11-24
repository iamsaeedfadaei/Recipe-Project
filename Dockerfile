# https://docs.docker.com/engine/reference/builder/

# using python in docker and who owns the project:
FROM python:3.8-alpine
MAINTAINER Saeed Fadaei Ltd

# WE use unbuffered cause we dont want any output to be buffered and make our project complicated.
ENV PYTHONUNBUFFERED 1 

# setting our requirements to docker:
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
# make directories for saving apps in docker and copy from local files:
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media  # -p: if dir does not exist then make it
RUN mkdir -p /vol/web/static
# making a user who works on project for secuirty issues:
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web  #the user(owner) has permission to do everything with the dir
USER user


# then in terminal of this project write:     docker build .