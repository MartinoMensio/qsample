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


docker build -t qsample .
docker run -it --rm --name qsample -p 8080:8080 qsample


# # run rest
# java -jar target/qsample-0.2.jar 