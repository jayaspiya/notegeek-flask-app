import os
from flask import Flask, render_template, url_for, redirect, request, flash, session
import model
app = Flask(__name__)
app.secret_key = "!#Top0Secret1Hash2Password"


if os.path.isfile("./notegeek.db") == False:
    model.createDB()


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        model.createNote(session["user"][0], title, description)
        flash(f"{title} Created")
        return redirect(url_for("home"))
    if "user" in session:
        notes = model.getAllNotes(session["user"][0])
        return render_template('index.html', username=session["username"], notes=notes)
    return redirect(url_for("login"))


@app.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        loggedUserId = model.getUserId(username, password)
        if loggedUserId is None:
            flash("Invalid Credential")
            return redirect(url_for("login"))
        session["user"] = loggedUserId
        session["username"] = username
        return redirect(url_for("home"))
    if "user" in session:
        return redirect(url_for("home"))
    return render_template('login.html')


@app.route('/signup/', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['uname']
        password = request.form['password']
        if model.addUser(username, fname, lname, password):
            flash("User Created!!!")
            return redirect(url_for("login"))
        flash("Username already exists")
        return redirect(url_for("signup"))
    if "user" in session:
        return redirect(url_for("home"))
    return render_template('signup.html')


@app.route("/<username>/<noteId>", methods=["POST", "GET"])
def update(username, noteId):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        model.updateNote(title, description, noteId, session["user"])
        return redirect(url_for("home"))
    if "user" in session:
        if username == session["username"]:
            note = model.getNote(noteId)
            return render_template("update.html", username=username, note=note, noteId=noteId)
    return "404 not found"


@app.route("/<username>/<noteId>/delete")
def delete(username, noteId):
    if "user" in session:
        if username == session["username"]:
            note = model.getNote(noteId)
            model.deleteNote(note[0])
            flash(f"'{note[1]}' deleted")
            return redirect(url_for("home"))
    return "404 not found"


@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
