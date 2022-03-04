# Using lightweight alpine image
FROM python:3.9-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/test

COPY ./Pipfile ./Pipfile.lock ./bin/run.sh ./
COPY ./app ./app

RUN chmod +x *.sh

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 5000

ENTRYPOINT ["/usr/src/test/bin/run.sh"]