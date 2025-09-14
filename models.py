from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    periodo = db.Column(db.String(2), nullable=False)
    sector = db.Column(db.String(20), nullable=False)
    nombre_consultor = db.Column(db.String(120), nullable=False)
    nombre_cliente = db.Column(db.String(160), nullable=False)
    origen_venta = db.Column(db.String(20), nullable=False)
    n_cotizacion_odoo = db.Column(db.String(60), nullable=True)
    n_licitacion = db.Column(db.String(60), nullable=True)
    tipo_servicio = db.Column(db.String(30), nullable=False)
    plazo_contrato = db.Column(db.Integer, nullable=False)
    tipo_venta = db.Column(db.String(30), nullable=False)
    fcv_nuevo = db.Column(db.Numeric(14,2), nullable=True)
    mrc_nuevo = db.Column(db.Numeric(14,2), nullable=True)
    fcv_renovado = db.Column(db.Numeric(14,2), nullable=True)
    mrc_inicial = db.Column(db.Numeric(14,2), nullable=True)
    mrc_final = db.Column(db.Numeric(14,2), nullable=True)
    variacion = db.Column(db.Numeric(14,2), nullable=True)
    pago_unico = db.Column(db.Numeric(14,2), nullable=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def recompute(self):
        def r2(x): return None if x is None else round(float(x),2)
        if self.fcv_nuevo is not None and self.plazo_contrato:
            self.mrc_nuevo = r2(float(self.fcv_nuevo)/int(self.plazo_contrato))
        else:
            self.mrc_nuevo = None
        if self.fcv_renovado is not None and self.plazo_contrato:
            self.mrc_final = r2(float(self.fcv_renovado)/int(self.plazo_contrato))
        else:
            self.mrc_final = None
        if self.mrc_final is not None and self.mrc_inicial is not None:
            self.variacion = r2(float(self.mrc_final)-float(self.mrc_inicial))
        else:
            self.variacion = None
