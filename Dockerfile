# https://docs.docker.com/engine/reference/builder/

# using python in docker and who owns the project:
FROM python:3.8-alpine
MAINTAINER Saeed Fadaei Ltd

# WE use unbuffered cause we dont want any output to be buffered and make our project complicated.
ENV PYTHONUNBUFFERED 1 

# setting our requirements to docker:
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# make directories for saving apps in docker and copy from local files:
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# making a user who works on project for secuirty issues:
RUN adduser -D user
USER user


# then in terminal of this project write:     docker build .