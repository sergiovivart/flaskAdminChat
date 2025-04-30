from flask import Blueprint, render_template, request, redirect, url_for, session

main = Blueprint('main', __name__)

# Dummy credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

@main.route("/")
def client():
    return render_template("client.html")

@main.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("main.login"))
    return render_template("admin.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("main.admin"))
        else:
            return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@main.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("main.login"))

