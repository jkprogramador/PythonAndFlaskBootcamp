from flask import Flask

app = Flask(__name__)


def convert_to_puppy_latin(name: str) -> str:
    """
    Return the puppy latin version of the given puppy name.

    If a puppy name does not end in a y, add y to the end.
    Ex.: Rufus -> Rufusy.

    If a puppy name does end in y, replace it with iful.
    Ex.: Sparky -> Sparkiful.
    """
    name = name.strip()

    if "y" == name[-1]:
        name = name[:-1] + "iful"
    else:
        name += "y"

    return name


@app.route("/")
def index():
    return "<h1>Welcome! Go to /puppy_latin/name to see your puppy latin name!</h1>"


@app.route("/information")
def info():
    return "<h1>Puppies are cute!</h1>"


@app.route("/puppy/<name>")
def puppy(name: str):
    return f"<h1>This is a page for {name.title()}</h1>"


@app.route("/puppy_latin/<name>")
def puppy_latin(name: str):
    puppy_latin_name = convert_to_puppy_latin(name)

    return f"<h1>Hi {name}! Your puppy latin name is {puppy_latin_name}</h1>"


if "__main__" == __name__:
    app.run(debug=True)
