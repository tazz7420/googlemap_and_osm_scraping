ARG CODE_VERSION=22.04
FROM ubuntu:${CODE_VERSION}
ARG DEBIAN_FRONTEND=noninteractive
LABEL maintainer='whats_for_lunch'

# switch working directory
WORKDIR /app

# 把目前目錄下的 ./app 複製到 /app
COPY ./app /app

# 安裝必要套件 (apt-get)
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y python3.10-dev && \
    apt-get install -y gdal-bin && \
    apt-get install -y libgdal-dev && \ 
    apt-get install -y g++

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py

# 安裝必要套件 (pip3 install -r 從檔案讀取要安裝的套件以及版本)
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "./whats_for_lunch.py" ]
