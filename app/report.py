from flask import Flask, request, jsonify

from logger import logger
from persist import CalcPersistenceInDB
from jsonprovider import CalcJSONProvider

Flask.json_provider_class = CalcJSONProvider
app = Flask(__name__)


@app.route("/report")
def report():
    url_parameters = request.args.to_dict()

    try:
        calculation_db = CalcPersistenceInDB()
        return jsonify(
            calculation_db.get_history_by_date(**url_parameters)
        )
    except Exception as err:
        logger.error(err)
        return jsonify([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)