from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "alpha"

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
