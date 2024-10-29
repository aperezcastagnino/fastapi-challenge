# FastApi Challenge

## Project setup
You only need to install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/).

In order to use the database found in the repository and to minimize the configuration required to run the project, please add the following environment variables:

```
# backend/.env

LOG_LEVEL=DEBUG
SERVER_URL=challenge-fastapi.com
ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_SIGNING_KEY=red_panda
```

```
# frontend/.env

API_BASE_URL=http://backend:8000/api/v1
```


## How to run:
To start the project you only need to do `docker-compose up`. Once the containers run, go to `http://localhost:8000/docs` to see the API documentation. Also, you can go to `http://localhost:8501` to access the website


## Good to Know:
You can use a VSCode extension to visualize the SQLite file.

