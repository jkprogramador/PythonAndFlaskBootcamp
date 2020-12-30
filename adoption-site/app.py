from myproject import app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")


if "__main__" == __name__:
    app.run(debug=True)
