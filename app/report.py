from flask import Flask, jsonify, request

from persistence import CalculationsDB
from utils import CalculatorJSONProvider, get_logger

app = Flask(__name__)
app.json = CalculatorJSONProvider(app)
logger = get_logger("report")


@app.route("/report")
def report():
    url_parameters = request.args.to_dict()
    calculations_db = CalculationsDB()

    try:
        return jsonify(
            calculations_db.get_calculations(**url_parameters)
        )
    except Exception as err:
        logger.error(err)
        return jsonify([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)