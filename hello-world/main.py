from flask import Flask, render_template, request, flash
import re

app = Flask(__name__)
# import os; print(os.urandom(16)) to generate the secret key
app.config["SECRET_KEY"] = b'\x07\x89a\x12\xfd\x04\xf5(6.\xc6\xe6\x895\x08n'


def convert_to_puppy_latin(name: str) -> str:
    """
    Return the puppy latin version of the given puppy name.

    If a puppy name does not end in a y, add y to the end.
    Ex.: Rufus -> Rufusy.

    If a puppy name does end in y, replace it with iful.
    Ex.: Sparky -> Sparkiful.

    :param name: The name of the puppy.
    :return: The puppy latin version of the given name.
    """
    name = name.strip()

    if "y" == name[-1]:
        name = name[:-1] + "iful"
    else:
        name += "y"

    return name


def check_username(username: str) -> list:
    """
    Check the given username for some requirements.

    Username must contain a lowercase letter.

    Username must contain a uppercase letter.

    Username must end in a number.

    :param username: A username.
    :return: A list of error messages for the requirements that were not satisfied;
        otherwise an empty list.
    """
    errors = []
    lowercase_letter_rgx = re.compile(r"[a-z]+")
    # or: any([c.islower() for c in username]) would return True if any is lower.
    uppercase_letter_rgx = re.compile(r"[A-Z]+")
    # or: any([c.isupper() for c in username]) would return True if any is upper.
    end_in_number_rgx = re.compile(r"[0-9]$")
    # or: username[-1].isdigit() would return True if ends in digit.

    if not lowercase_letter_rgx.search(username):
        errors.append("Username must contain at least one lowercase letter.")
    if not uppercase_letter_rgx.search(username):
        errors.append("Username must contain at least one uppercase letter.")
    if not end_in_number_rgx.search(username):
        errors.append("Username must end in a number.")

    return errors


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/information")
def info():
    name = "Jack"
    letters = list(name)
    pup_dict = {"pup_name": "Zezinho"}

    return render_template("information.html", name=name, letters=letters,
                           pup_dict=pup_dict)


@app.route("/puppy/<name>")
def puppy(name: str):
    return f"<h1>This is a page for {name.title()}</h1>"


@app.route("/puppy_latin/<name>")
def puppy_latin(name: str):
    puppy_latin_name = convert_to_puppy_latin(name)

    return f"<h1>Hi {name.strip()}! Your puppy latin name is {puppy_latin_name}</h1>"


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/thank-you")
def thank_you():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")

    return render_template("thank_you.html", firstname=firstname,
                           lastname=lastname)


@app.route("/username-form", methods=["GET", "POST"])
def username_form():
    errors = []

    if "POST" == request.method:
        username = request.form.get("username")
        errors = check_username(username)

        if not errors:
            flash(f"Your username {username} is allowed.")

    return render_template("username_form.html", errors=errors)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if "__main__" == __name__:
    app.run(debug=True)
