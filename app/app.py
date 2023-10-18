import datetime
import mysql.connector

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)

@app.route("/calculate")
def calculate():
    args = request.args
    form = args.get("form")
    json = args.get("json")

    method = args.get("method")
    value1 = args.get("value1", type=int)
    value2 = args.get("value2", type=int)

    result = (value1 + value2 if method == "sum"
         else value1 - value2 if method == "subb"
         else value1 * value2 if method == "multiply"
         else value1 / value2 if method == "divide" and value2 != 0
         else None)

    status = "ok" if result != None else "error"

    if form == "sent":
        try:
            mysql_database = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="history_db"
            )
            mysql_cursor = mysql_database.cursor()

            date = datetime.datetime.utcnow()

            add_record = ("INSERT INTO history_tb "
                          "(METHOD, VALUE1, VALUE2, RESULT, STATUS, DATE)"
                          "VALUES (%s, %s, %s, %s, %s, %s)")

            data = (method, value1, value2, result, status, date)

            mysql_cursor.execute(add_record, data)
            mysql_database.commit()

        except mysql.connector.Error as err:
            print(err.msg)

        finally:
            mysql_cursor.close()
            mysql_database.close()

    if json == "true":
        return jsonify({
            "method": method,
            "status": status,
            "result": result
        })

    return render_template("index.html", result = result)


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
                "date": line[5].isoformat(sep=" "),
                "operation": line[0],
                "result": line[3],
                "status": line[4],
                "value1": line[1],
                "value2": line[2]
            }
            i += 1

    except mysql.connector.Error as err:
        print(err.msg)

    finally:
        mysql_cursor.close()
        mysql_database.close()

    return jsonify(history)
