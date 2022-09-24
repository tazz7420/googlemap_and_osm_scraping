#!/bin/bash

docker build -t xinzhe/docker_whatsforlunch_v7 .
docker container run -d --name docker_whatsforlunch_v7 xinzhe/docker_whatsforlunch_v7

