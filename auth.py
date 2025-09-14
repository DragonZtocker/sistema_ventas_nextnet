from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, LoginManager
from models import db, User

bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Bienvenido, " + username, "success")
            return redirect(url_for("ventas.listar_ventas"))
        flash("Credenciales inválidas", "danger")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("auth.login"))
