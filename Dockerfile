FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python python-pip cron
RUN pip install flask scapy
COPY . /opt/
WORKDIR /opt
RUN chmod +x entrypoint.sh
ENTRYPOINT /bin/bash ./entrypoint.sh