from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class VentaForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired()])
    periodo = SelectField("Periodo", choices=[("Q1","Q1"),("Q2","Q2"),("Q3","Q3"),("Q4","Q4")], validators=[DataRequired()])
    sector = SelectField("Sector", choices=[("Lima","Lima"),("Provincia","Provincia")], validators=[DataRequired()])
    nombre_consultor = StringField("Nombre Consultor", validators=[DataRequired()])
    nombre_cliente = StringField("Nombre Cliente", validators=[DataRequired()])
    origen_venta = SelectField("Origen de Venta", choices=[("Cotizacion","Cotizacion"),("Licitacion","Licitacion")], validators=[DataRequired()])
    n_cotizacion_odoo = StringField("N° Cotizacion Odoo", validators=[Optional()])
    n_licitacion = StringField("N° Licitacion", validators=[Optional()])
    tipo_servicio = SelectField("Tipo de Servicio", choices=[("Datos","Datos"),("Internet","Internet"),("Telefonía","Telefonía"),("Datacenter","Datacenter")], validators=[DataRequired()])
    plazo_contrato = IntegerField("Plazo Contrato (meses)", validators=[DataRequired(), NumberRange(min=1, max=100)])
    tipo_venta = SelectField("Tipo de Venta", choices=[("Venta Nueva","Venta Nueva"),("Renovacion Cero","Renovacion Cero"),("Renovacion Alta","Renovacion Alta"),("Renovacion Baja","Renovacion Baja")], validators=[DataRequired()])
    fcv_nuevo = DecimalField("FCV Nuevo", places=2, validators=[Optional()])
    mrc_nuevo = DecimalField("MRC Nuevo (auto)", places=2, validators=[Optional()])
    fcv_renovado = DecimalField("FCV Renovado", places=2, validators=[Optional()])
    mrc_inicial = DecimalField("MRC Inicial", places=2, validators=[Optional()])
    mrc_final = DecimalField("MRC Final (auto)", places=2, validators=[Optional()])
    variacion = DecimalField("Variación (auto)", places=2, validators=[Optional()])
    pago_unico = DecimalField("Pago Único", places=2, validators=[Optional()])
    submit = SubmitField("Guardar")
