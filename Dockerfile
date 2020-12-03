#Dockerfile

FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=True
ENV PYTHONUNBUFFERED 1 

# running Pipfile
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system

# creating a dir on the Docker image
COPY . /app/
EXPOSE 8000 

# docker run -d -e SECRET_KEY="key" app
# docker run -d --env-file .env app

