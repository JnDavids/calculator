from flask import Flask, request, jsonify, render_template
from confluent_kafka import Producer

from logger import logger
from calculator import Calculator
from jsonprovider import CalcJSONProvider

Flask.json_provider_class = CalcJSONProvider

app = Flask(__name__)
calculator = Calculator()
producer = Producer({ "bootstrap.servers": "kafka:9092" })


@app.route("/")
def index():
    url_parameters = request.args.to_dict()

    try:
        calculation = calculator.calculate(**url_parameters)
    except Exception as err:
        return jsonify(error=str(err))

    try:
        producer.produce("calculations", app.json.dumps(calculation))
    except Exception as err:
        logger.error(err)

    return jsonify(calculation)


@app.route("/calculate")
def calculate():
    url_parameters = request.args.to_dict()

    try:
        calculation = calculator.calculate(**url_parameters)
        result = calculation.result
    except Exception as err:
        if any(
            parameter in url_parameters
            for parameter in ("operation", "value_1", "value_2")
        ):
            result = str(err)
        else:
            result = None
    else:
        try:
            producer.produce("calculations", app.json.dumps(calculation))
        except Exception as err:
            logger.error(err)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)