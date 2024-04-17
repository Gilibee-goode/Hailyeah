#!/bin/bash  

docker build . -t gilibee/hailyeah

docker tag gilibee/hailyeah gilibee/hailyeah:latest
#docker tag gilibee/hailyeah gilibee/hailyeah_private:latest

docker push gilibee/hailyeah:latest
#docker push gilibee/hailyeah_private:latest
