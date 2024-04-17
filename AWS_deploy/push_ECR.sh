#!/bin/bash

aws ecr get-login-password --region il-central-1 | docker login --username AWS --password-stdin 058264276766.dkr.ecr.il-central-1.amazonaws.com


 
docker tag hailyeah:latest 058264276766.dkr.ecr.il-central-1.amazonaws.com/hailyeah:latest
 
docker push 058264276766.dkr.ecr.il-central-1.amazonaws.com/hailyeah:latest
 
 
