from flask import Flask, render_template
from forms import InfoForm

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


if "__main__" == __name__:
    app.run(debug=True)
