#!/bin/sh
set -e

# build JAR

# git clone https://github.com/christianscheible/qsample.git
# cd qsample
mvn compile
mvn package


# models

# wget https://github.com/christianscheible/qsample/releases/download/0.1/models.tar.gz
tar xzfv models.tar.gz


# # run (OLD)
# java -jar target/qsample-0.1-jar-with-dependencies.jar --sample example/documents/ output


docker build -t martinomensio/qsample .
docker run -it --name qsample -p 8080:8080 martinomensio/qsample
# docker start qsample


# # run rest without docker
# java -jar target/qsample-0.2.jar 