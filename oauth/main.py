from flask import Flask, render_template, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import os

# Indicates that you are doing local testing and it's OK to use HTTP instead of
# HTTPS for OAuth.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Indicates that it's OK for Google to return different OAuth scopes than requested.
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# Go to https://console.developers.google.com/ to create app with these credentials.
# Follow the instructions at https://github.com/singingwolfboy/flask-dance-google.
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""

app = Flask(__name__)
app.config["SECRET_KEY"] = b'\xac\x18/8\x9c\x0bt*\xdd8\x031-\xe3\x1b{'

blueprint = make_google_blueprint(client_id=GOOGLE_CLIENT_ID,
                                  client_secret=GOOGLE_CLIENT_SECRET,
                                  offline=True,
                                  scope=["profile", "email"])
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/google")
def login():
    if not google.authorized:
        return render_template(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")

    assert resp.ok, resp.text

    email = resp.json()["email"]

    return render_template("welcome.html", email=email)


@app.route("/welcome")
def welcome():
    # Return 500 error if not logged in, as an example.
    resp = google.get("/oauth2/v2/userinfo")

    assert resp.ok, resp.text

    email = resp.json()["email"]

    return render_template("welcome.html", email=email)


if "__main__" == __name__:
    app.run()
