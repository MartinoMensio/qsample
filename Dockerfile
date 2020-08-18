from openjdk

COPY ./target/qsample-0.2.jar /app/qsample-0.2.jar
COPY ./resources /app/resources
WORKDIR /app
CMD ["java", "-jar", "qsample-0.2.jar"]
