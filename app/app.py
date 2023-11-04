from flask import Flask, request as req, jsonify, render_template
from flask_executor import Executor

from logger import logger
from persist import CalcPersistenceInDB
from calculator import Calculator
from jsonprovider import CalcJSONProvider

Flask.json_provider_class = CalcJSONProvider

app = Flask(__name__)
executor = Executor(app)


@app.route("/calculate")
def calculate():
    form = req.args.get("form")
    json = req.args.get("json")

    operation = req.args.get("operation")
    value1 = req.args.get("value1", type=int)
    value2 = req.args.get("value2", type=int)
    result = None

    if form == "sent":
        try:
            calculation = Calculator(operation, value1, value2)
            result = calculation.result
        except Exception as err:
            return jsonify(error=str(err))

        try:
            calculation_db = CalcPersistenceInDB()
            executor.submit(calculation_db.persist(calculation))
        except Exception as err:
            logger.error(err)

        if json == "true":
            return jsonify(calculation.as_dict)

    return render_template("index.html", result=result)


@app.route("/report")
def report():
    initial_date = req.args.get("i_date")
    final_date = req.args.get("f_date")

    try:
        calculation_db = CalcPersistenceInDB()
        return jsonify(
            calculation_db.get_history_by_date(initial_date, final_date)
        )
    except Exception as err:
        logger.error(err)
        return jsonify([])