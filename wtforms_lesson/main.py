from flask import Flask, render_template, session, redirect, url_for, flash
from forms import InfoForm, MyForm

app = Flask(__name__)
app.config[
    "SECRET_KEY"] = b'\xf5\xfb\xf6F\x8f\\\xd5\xc1\x1b\x93\xfe\xfc\xaa\xd1\xb0\xdc'


@app.route("/", methods=["GET", "POST"])
def index():
    breed = False
    form = InfoForm()

    if form.validate_on_submit():
        breed = form.breed.data
        form.breed.data = ""

    return render_template("index.html", form=form, breed=breed)


@app.route("/my-form", methods=["GET", "POST"])
def my_form():
    form = MyForm()

    if form.validate_on_submit():
        session["breed"] = form.breed.data
        session["neutered"] = form.neutered.data
        session["mood"] = form.mood.data
        session["food_choice"] = form.food_choice.data
        session["feedback"] = form.feedback.data
        flash("Thank you!!!")

        return redirect(url_for("thank_you"))

    return render_template("my_form.html", form=form)


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


if "__main__" == __name__:
    app.run(debug=True)
