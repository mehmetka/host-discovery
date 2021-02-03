#!/bin/bash

echo "Web App has been started"

FLASK_APP=/opt/app.py 
nohup flask run --host=0.0.0.0 --port=8080 > log.txt 2>&1 &

echo "Docker container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

echo "SHELL=/bin/bash
BASH_ENV=/container.env
0 1 * * * python /opt/worker.py >> /opt/worker.log 2>&1" > scheduler.txt

crontab scheduler.txt
cron -f