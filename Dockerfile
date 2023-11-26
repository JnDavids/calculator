FROM python

RUN pip install locust
RUN pip install Flask
RUN pip install mysql-connector-python
RUN pip install confluent-kafka

WORKDIR /app

EXPOSE 8089
EXPOSE 5000
EXPOSE 5001

ENTRYPOINT ["/bin/tail", "-f", "/dev/null"]