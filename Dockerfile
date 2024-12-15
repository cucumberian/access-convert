FROM python:3.13-slim-bullseye

RUN apt-get update && apt-get install -y locales locales-all --no-install-recommends
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get install mdbtools zip --no-install-recommends -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data/
WORKDIR /data/


COPY access2csv.sh /usr/local/bin/access2csv.sh
RUN chmod +x /usr/local/bin/access2csv.sh


RUN mkdir /app/
COPY /app/requirements.txt /app/
RUN pip3 install --no-cache -r /app/requirements.txt
COPY ./app/ /app/
WORKDIR /app/

ENTRYPOINT [ "uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
