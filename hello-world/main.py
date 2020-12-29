from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello Puppy!</h1>"


if "__main__" == __name__:
    app.run(debug=True)
