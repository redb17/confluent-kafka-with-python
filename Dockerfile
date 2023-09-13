FROM ubuntu

WORKDIR /home
RUN apt-get update && apt upgrade -y
RUN apt-get install curl -y
RUN apt install default-jdk -y
COPY ./*.py .
# Latest confluent version: https://docs.confluent.io/platform/current/installation/installing_cp/zip-tar.html
RUN curl -O https://packages.confluent.io/archive/7.5/confluent-7.5.0.tar.gz
RUN tar xvzf confluent-7.5.0.tar.gz
RUN rm confluent-7.5.0.tar.gz
RUN apt-get install python3-pip -y
RUN pip install confluent-kafka
