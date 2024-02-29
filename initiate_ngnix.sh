#!/bin/bash

# starts ngnix deamon
nginx -g "daemon off;" &
source .venv/bin/activate && .venv/bin/python3 -m gunicorn -w 3 --bind=0.0.0.0:8000 --bind=0.0.0.0:8001 Hail_yeah_weather_API:hailyeah &

wait -n

#source /app/.venv/bin/activate
#source /app/.venv/bin/gunicorn -w 3 --bind=0.0.0.0:8000 Hail_yeah_weather_API:hailyeah

