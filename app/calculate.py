from flask import Flask, request, jsonify, render_template
from flask_executor import Executor

from logger import logger
from persist import CalcPersistenceInDB
from calculator import Calculator
from jsonprovider import CalcJSONProvider

Flask.json_provider_class = CalcJSONProvider

app = Flask(__name__)
executor = Executor(app)
calculator = Calculator()


@app.route("/")
def index():
    url_parameters = request.args.to_dict()

    try:
        calculation = calculator.calculate(**url_parameters)
    except Exception as err:
        return jsonify(error=str(err))
    else:
        try:
            calculation_db = CalcPersistenceInDB()
            executor.submit(calculation_db.persist(calculation))
        except Exception as err:
            logger.error(err)

        return jsonify(calculation.to_dict())


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
            calculation_db = CalcPersistenceInDB()
            executor.submit(calculation_db.persist(calculation))
        except Exception as err:
            logger.error(err)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)