# Setup
Streamlite consists of a FastAPI app (REST API) with PostegreSQL database in a Docker multicontainer.

## Install Docker
Install Docker Desktop here: https://docs.docker.com/desktop/install/windows-install/

## Build and launch app & database
```
docker build -t streamlite .
docker-compose up
```
