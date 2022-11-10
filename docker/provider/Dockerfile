# pull official base image
FROM python:3.10-slim

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./provider/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./provider/ /code/
RUN ls -la
WORKDIR /code

ADD ./docker/provider/entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
