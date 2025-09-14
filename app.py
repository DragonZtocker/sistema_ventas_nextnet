from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from models import db, User
from auth import bp as auth_bp, login_manager
from ventas import bp as ventas_bp
from reports import bp as reportes_bp
from config import ProdConfig
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder="templates", static_folder="static")
    app.config.from_object(ProdConfig())
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(reportes_bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("ventas.listar_ventas"))
        return redirect(url_for("auth.login"))

    @app.template_filter("money")
    def money(v):
        try:
            return f"{float(v or 0):.2f}"
        except:
            return "0.00"

    with app.app_context():
        from models import Venta
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
        if not User.query.filter_by(username="rlizarbe").first():
            u = User(username="rlizarbe", role="user")
            u.set_password("141215")
            db.session.add(u)
        if not User.query.filter_by(username="invitado").first():
            g = User(username="invitado", role="guest")
            g.set_password("guest")
            db.session.add(g)
        db.session.commit()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
