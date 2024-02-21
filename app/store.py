import json
import os

from confluent_kafka import Consumer

from persistence import CalculationsDB
from utils import get_logger


def main():
    calculations_db = CalculationsDB()
    logger = get_logger("store")

    try:
        consumer = Consumer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER"),
            "group.id": "calc_consumers",
            "auto.offset.reset": "earliest"
        })
        consumer.subscribe([os.getenv("KAFKA_TOPIC")])
    except Exception as err:
        logger.error(err)
        return

    while True:
        msg = consumer.poll()

        if msg and not msg.error():
            try:
                calculation = json.loads(msg.value())
                calculations_db.insert(calculation)
            except Exception as err:
                logger.error(err)


if __name__ == "__main__":
    main()