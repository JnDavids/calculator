import json

from confluent_kafka import Consumer
from persist import CalcPersistenceInDB
from logger import logger

consumer = Consumer({
    "bootstrap.servers": "kafka:9092",
    "group.id": "calc_consumers",
    "auto.offset.reset": "earliest"
})
calculations_db = CalcPersistenceInDB()

consumer.subscribe(["calculations"])

while True:
    msg = consumer.poll()

    if not msg.error():
        try:
            calculation = json.loads(msg.value())
            calculations_db.persist(calculation)
        except Exception as err:
            logger.error(err)