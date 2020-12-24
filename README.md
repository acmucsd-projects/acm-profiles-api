# acm-profiles-api
ACM Profiles API (Side Projects Sage Team)

REST API for ACM Profiles. Built using Django and PostgreSQL.

## Required Dependencies
1. Python 3 and pip - [instructions](https://www.python.org/downloads/)
2. Docker - [instructions](https://docs.docker.com/get-docker/)
3. docker-compose - [instructions](https://docs.docker.com/compose/install/)
4. PostgreSQL - [instructions](https://www.postgresql.org/download/)

## Build instructions
1.  Install pipenv, a tool which automates virtual environments for python.
2.  Clone the repository: `git@github.com:acmucsd/acm-profiles-api.git`
3.  Navigate to the project directory: `cd acm-profiles-api`
4.  Create `.env` file, using [`.env.example`](https://github.com/acmucsd/acm-profiles-api/blob/main/.env.example) as a template : `cp .env.example .env`.
5.  Fill out the `.env`. See the example file below.
6.  Run `pipenv install` to install all the dependencies and `pipenv shell` to activate the virtual environment.
7.  Run the docker container: `docker-compose up -d`.
8.  Run the local testing server: `python manage.py runserver`.

## Sample `.env` file:

```
SECRET_KEY=secret_key
DATABASE_URL=postgres://trrrbyrqkcgsdl:e2ee1b38fec8d3c6ce76efdb267b1d950c2ea474d3352c1e5893990634f88963@ec2-34-204-121-199.compute-1.amazonaws.com:5432/df1u5kk38d47cf
DOCKER_DB_PORT=5433
DOCKER_DB_NAME=example_db_name
DOCKER_DB_USER=postgres_admin_user
DOCKER_DB_PASSWORD=postgres_admin_password
MEMBERSHIP_PORTAL_API=localhost:8080/

```
