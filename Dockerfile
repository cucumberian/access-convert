FROM python:3.13-slim-bullseye

RUN apt-get update && apt-get install -y locales locales-all --no-install-recommends
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get install mdbtools --no-install-recommends -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data/
WORKDIR /data/


COPY access2csv.sh /usr/local/bin/access2csv.sh
RUN chmod +x /usr/local/bin/access2csv.sh

ENTRYPOINT [ "access2csv.sh" ]
