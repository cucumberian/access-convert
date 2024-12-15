# Access database to sql via Docker-container

## Description

Transform access database to schema, csv files and sql files.
Convert via web-interface with download result as zip archive.

## Install

Build docker image

```sh
docker build --tag access-fastapi .
```

## Usage

Run docker image and connect database file via volume

```sh
docker run -d --rm -p "80:8000" access-fastapi
```

Use browser to access host machine port 80.
