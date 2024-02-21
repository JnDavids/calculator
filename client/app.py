import json
from urllib.request import HTTPError, urlopen

from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/calculate")
def calculate():
    query = request.args.to_dict()
    status = None
    result = None

    if any(arg in query
           for arg in ("operation", "value_1", "value_2")):

        try:
            response = urlopen(f"http://nginx:80{request.full_path}")
        except HTTPError as err:
            result = json.loads(err.read().decode())["error"]
            status = "error"
        else:
            result = json.loads(response.read().decode())
            status = "ok"
            operation = result["operation"]

            for number in ("value_1", "value_2", "result"):
                if result[number] >= 10 ** 12:
                    result[number] = f"{result[number]:.2e}"
                    continue

                if float(result[number]).is_integer():
                    result[number] = int(result[number])
                
                result[number] = f"{result[number]:,}"

            result["operation"] = ("+" if operation == "sum" 
                              else "-" if operation == "subb"
                              else "x" if operation == "multiply"
                              else "/")

    return render_template(
        "index.html",
        result=result,
        status=status,
        style=url_for("static", filename="css/style.css"),
        script=url_for("static", filename="js/index.js")
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4321)