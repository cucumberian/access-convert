# Access database to sql via Docker-container

## Description

Transfer access file database to postgres

## Install

Build docker image

```sh
docker build --tag access-csv .
```

## Usage

Run docker image and connect database file via volume

```sh
docker run --rm \
-v "./access/:/data/" \
access-csv access_base.accdb /data/out/ 
```

### Where

- `./access/` - directory with access file `access_base.accdb`
- `/data/out/` - directory with output csv files and sql schema
- `access_base.accdb` - access database
- `other_docker_network` - use when you need connect to postgres in container
