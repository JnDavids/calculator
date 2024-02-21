import os

from confluent_kafka import Producer
from flask import Flask, jsonify, request

from calculator import Calculator
from utils import CalculatorJSONProvider, get_logger

app = Flask(__name__)
app.json = CalculatorJSONProvider(app)

logger = get_logger("calculate")

producer = Producer({
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER")
})


@app.route("/calculate")
def index():
    url_parameters = request.args.to_dict()

    try:
        calculation = Calculator.calculate(**url_parameters)
    except Exception as err:
        return jsonify(error=str(err)), 400

    try:
        producer.produce(
            os.getenv("KAFKA_TOPIC"), app.json.dumps(calculation)
        )
    except Exception as err:
        logger.error(err)

    return jsonify(calculation)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)