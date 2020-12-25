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
6.  Run `pipenv sync` to install all the dependencies and `pipenv shell` to activate the virtual environment.
7.  Run the docker container: `docker-compose up -d`.
8.  Make migrations to the database: `python manage.py migrate`.
9.  Load the test data: `python manage.py loaddata */fixtures/*.json`.
10. Run the local testing server: `python manage.py runserver`.
11. Follow setup instructions for the [`membership portal api`](https://github.com/acmucsd/membership-portal)

Make sure that your databases for acm profiles and the membership portal are running on different ports. As a suggestion, use 5433 for acm profiles and 5432 for the membership portal. The two servers need to run on different ports as well. ACM profiles defaults to 8000, so run the membership portal on a different port, such as 3000.

## Sample `.env` file:

```
SECRET_KEY=secret_key
DATABASE_URL='postgres://name:password@localhost:5433/user'
DOCKER_DB_PORT='5433'
DOCKER_DB_NAME='name'
DOCKER_DB_USER='user'
DOCKER_DB_PASSWORD='password
MEMBERSHIP_PORTAL_API='http://localhost:3000/'

```
