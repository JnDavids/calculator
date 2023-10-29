import logging
import mysql.connector

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_executor import Executor

from calculator import Calculator


logger = logging.getLogger("calculator")

log_format = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)

log_handler = logging.FileHandler("./log/app.log")
log_handler.setFormatter(log_format)

logger.addHandler(log_handler)


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

            executor.submit(insert_record, calculation)

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
        mysql_database = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            database="history_db"
        )
        mysql_cursor = mysql_database.cursor()
        mysql_cursor.execute("SELECT * FROM history_tb")

        for line in mysql_cursor:
            history[i] = {
                "operation": line[0],
                "value1": line[1],
                "value2": line[2],
                "result": line[3],
                "date": line[4].isoformat(sep=" ")
            }
            i += 1

    except mysql.connector.Error as err:
        logger.error(err)

    finally:
        mysql_cursor.close()
        mysql_database.close()

    return jsonify(history)


def insert_record(calculator):
    try:
        mysql_database = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            database="history_db"
        )
        mysql_cursor = mysql_database.cursor()

        add_record = ("INSERT INTO history_tb "
                      "(METHOD, VALUE1, VALUE2, RESULT, DATE)"
                      "VALUES (%s, %s, %s, %s, %s)")

        data = (calculator.get_operation(),
                calculator.get_value1(),
                calculator.get_value2(),
                calculator.get_result(),
                calculator.get_date())

        mysql_cursor.execute(add_record, data)
        mysql_database.commit()

    except mysql.connector.Error as err:
        logger.error(err)

    finally:
        mysql_cursor.close()
        mysql_database.close()