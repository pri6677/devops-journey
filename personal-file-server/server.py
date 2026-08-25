from flask import (
    Flask,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
    session
)

from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import os


# -------------------------
# Load environment variables
# -------------------------

load_dotenv(override=True)


# -------------------------
# Flask application
# -------------------------

app = Flask(__name__)

# Secret key from .env
app.secret_key = os.getenv("SECRET_KEY")


# -------------------------
# File storage
# -------------------------

UPLOAD_FOLDER = "server-files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------
# Login credentials
# -------------------------

USERNAME = os.getenv("USERNAME")

PASSWORD_HASH = os.getenv("PASSWORD_HASH")


# -------------------------
# Login
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and check_password_hash(
            PASSWORD_HASH,
            password
        ):

            session["logged_in"] = True

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# -------------------------
# Logout
# -------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -------------------------
# Dashboard
# -------------------------

@app.route("/")
def home():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    files = os.listdir(UPLOAD_FOLDER)

    return render_template(
        "index.html",
        files=files
    )


# -------------------------
# Upload
# -------------------------

@app.route("/upload", methods=["POST"])
def upload():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    file = request.files["file"]

    if file.filename:

        filename = secure_filename(file.filename)

        if filename:

            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
            )

    return redirect(url_for("home"))


# -------------------------
# Download
# -------------------------

@app.route("/download/<filename>")
def download(filename):

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )


# -------------------------
# Delete
# -------------------------

@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.exists(file_path):

        os.remove(file_path)

    return redirect(url_for("home"))


# -------------------------
# Start server
# -------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000
    )