FROM python:3.12

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 5001

ENTRYPOINT ["sleep", "infinity"]