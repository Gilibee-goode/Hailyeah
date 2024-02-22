 #!/bin/bash
container_name=hailyeah

#ECR Login
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 058264276766.dkr.ecr.eu-north-1.amazonaws.com

#Pulling image from ECR
docker pull 058264276766.dkr.ecr.eu-north-1.amazonaws.com/hailyeah:latest

##Changing image tag
docker image tag 058264276766.dkr.ecr.eu-north-1.amazonaws.com/hailyeah:latest $container_name:latest

#stop and remove the current container
docker rm -f $container_name || true

#Creating and starting a docker container using a new image
docker run -d --restart unless-stopped -p 80:80 --name $container_name $container_name:latest
