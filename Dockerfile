# Use the official Python image from the DockerHub
FROM python:3.10-slim

# Set the working directory in docker
#WORKDIR /app

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Copy the dependencies file to the working directory
#COPY requirements.txt .

# Install any dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
#COPY . .

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential
#RUN apt-get install libreoffice
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# # base image
# FROM python:3.9.7-buster
 
# # options
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
 
# # Set working directory
# RUN mkdir intellidoc
# # set the working directory
# COPY . /intellidoc/
# # coppy commands 
# WORKDIR /intellidoc
 
# # update docker-iamage packages
# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y netcat-openbsd gcc && \
#     apt-get clean
 
# # update pip 
# RUN pip install --upgrade pip
# # install psycopg for connect to pgsql
# RUN pip install psycopg2-binary
# # install python packages 
# RUN pip install -r requirements.txt
# # create static directory
# #RUN mkdir static
# # RUN python manage.py collectstatic --no-input
# EXPOSE 8000
# CMD ["gunicorn","--bind", ":8000", "intellidoc.wsgi:application"]