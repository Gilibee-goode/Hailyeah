
FROM ubuntu:latest AS build

RUN apt update && apt install -y python3 python3-venv python3-pip
RUN mkdir /API_Project
WORKDIR /API_Project

# create a venv to store all dependencies for the project
RUN python3 -m venv .venv  

#RUN ./.venv/bin/activate && pip install gunicorn Flask requests
RUN . .venv/bin/activate && pip install gunicorn Flask requests boto3 prometheus_flask_exporter

COPY API_Project /API_Project

#RUN useradd -ms /bin/bash hailyeah

#USER hailyeah
#WORKDIR /home/hailyeah/API_Project/




FROM ubuntu

RUN apt update -y && apt install -y nginx python3 

COPY --from=build /API_Project /app


COPY run_gunicorn.sh /app/run_gunicorn.sh 

WORKDIR /app
CMD ["bash", "run_gunicorn.sh"]


