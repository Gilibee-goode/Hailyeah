
FROM ubuntu:latest AS build

RUN apt update && apt install -y python3 python3-venv python3-pip

COPY API_Project /API_Project

WORKDIR /API_Project

# create a venv to store all dependencies for the project
RUN python3 -m venv .venv  

#RUN ./.venv/bin/activate && pip install gunicorn Flask requests
RUN . .venv/bin/activate && pip install gunicorn Flask requests

#RUN useradd -ms /bin/bash hailyeah

#USER hailyeah
#WORKDIR /home/hailyeah/API_Project/




FROM ubuntu

COPY --from=build /API_Project /app

RUN apt update -y && apt install -y nginx python3

COPY API_Project/ngnix_config_file.conf /etc/nginx/sites-enabled/default

COPY initiate_ngnix.sh /app/initiate_ngnix.sh 

RUN chmod 544 /app/initiate_ngnix.sh 
WORKDIR /app
CMD ["bash", "initiate_ngnix.sh"]


