from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "alpha"

database_path = os.path.join(os.path.dirname(__file__), 'app.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{database_path}'
database = SQLAlchemy(app)


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), unique=True, nullable=False)

database.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        session["username"] = None
        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect("/tasks")

    return render_template("login.html")


@app.route("/task")
def task():
    login_user = session["username"]
    return render_template("task.html", username=login_user)


if __name__ == "__main__":
    app.run(debug=True)
