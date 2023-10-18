FROM python

RUN pip install locust
RUN pip install Flask
RUN pip install mysql-connector-python

WORKDIR /app
COPY ./app .

EXPOSE 8089
EXPOSE 5000

CMD flask --app app run --host=0.0.0.0