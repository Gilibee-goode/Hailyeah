#!/bin/bash

source .venv/bin/activate && .venv/bin/python3 -m gunicorn -w 3 --bind=0.0.0.0:80 Hail_yeah_weather_API:hailyeah

