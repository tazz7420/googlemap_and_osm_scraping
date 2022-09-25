#!/bin/bash

docker build -t xinzhe/docker_whatsforlunch_v7 .
docker container run -it  xinzhe/docker_whatsforlunch_v7

