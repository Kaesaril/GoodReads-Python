from flask import render_template, redirect, url_for, request , flash
from flask_login import login_user, logout_user
from . import auth_bp
import sirope
from src.models.usuario import Usuario

srp = sirope.Sirope()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        user = next(srp.filter(Usuario, lambda u: u.email == email), None)
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect(url_for("books.home"))  
        flash("No estas registrado", "error")
        return render_template("register.html")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        if next(srp.filter(Usuario, lambda u: u.email == email), None):
            flash("Este email ya está registrado", "error")
            return render_template("login.html")
        usuario = Usuario(request.form["nombre"], email, request.form["password"])
        srp.save(usuario)
        return redirect(url_for("auth.login"))
    return render_template("register.html")
