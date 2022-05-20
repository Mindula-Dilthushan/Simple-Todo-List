from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import enum
import os

app = Flask(__name__)
app.secret_key = "alpha"

database_path = os.path.join(os.path.dirname(__file__), 'app.db')

app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{database_path}'
database = SQLAlchemy(app)


class User(database.Model):
    user_id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), unique=True, nullable=False)
    tasks = database.relationship("Task", backref="user", lazy=True)


class TaskStatus(enum.Enum):
    COMPLETED = "Completed"
    CLOSED = "Closed"
    OPENED = "Opened"


class Task(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    task = database.Column(database.String(250), nullable=False)
    status = database.Column(database.Enum(TaskStatus), default=TaskStatus.OPENED)
    # user_id = database.Column(database.Integer, database.ForeignKey("user_id"), nullable=False)


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
