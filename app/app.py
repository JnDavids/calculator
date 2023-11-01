from flask import Flask, request, jsonify, render_template
from flask_executor import Executor

from logger import logger
from database import Database
from calculator import Calculator

app = Flask(__name__)
executor = Executor(app)


@app.route("/calculate")
def calculate():
    args = request.args
    form = args.get("form")
    json = args.get("json")

    method = args.get("method")
    value1 = args.get("value1", type=int)
    value2 = args.get("value2", type=int)

    if form == "sent":
        try:
            calculation = Calculator(method, value1, value2)

            try:
                data = (
                    calculation.get_operation(),
                    calculation.get_value1(),
                    calculation.get_value2(),
                    calculation.get_result(),
                    calculation.get_date().isoformat()
                )
            
                database = Database("mysql", "root", "root", "history_db")

                executor.submit(database.insert("history_tb", "*", data))
            except Exception as err:
                logger.error(err)

            if json == "true":
                return jsonify({
                    "method": calculation.get_operation(),
                    "value1": calculation.get_value1(),
                    "value2": calculation.get_value2(),
                    "result": calculation.get_result(),
                    "date": calculation.get_date()
                })

            return render_template("index.html", result = calculation.get_result())
        
        except Exception as err:
            return jsonify({ "error": str(err) })
    
    return render_template("index.html", result = None)


@app.route("/report")
def report():
    history = {}
    i = 0

    try:
        database = Database("mysql", "root", "root", "history_db")

        for row in database.select("history_tb"):
            history[i] = {
                "operation": row[0],
                "value1": row[1],
                "value2": row[2],
                "result": row[3],
                "date": row[4].isoformat(sep=" ")
            }
            i += 1

    except Exception as err:
        logger.error(err)

    return jsonify(history)