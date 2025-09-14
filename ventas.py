
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import date, datetime
from models import db, Venta
from forms import VentaForm

bp = Blueprint("ventas", __name__, url_prefix="/ventas")

def require_role(roles):
    def wrapper(func):
        from functools import wraps
        @wraps(func)
        def inner(*args, **kwargs):
            if not current_user.is_authenticated:
                from flask import redirect, url_for
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                flash("No tiene permisos para realizar esta acción.", "warning")
                return redirect(url_for("ventas.listar_ventas"))
            return func(*args, **kwargs)
        return inner
    return wrapper

def _parse_date(val):
    if not val: return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(val, fmt).date()
        except:
            pass
    return None

@bp.route("/")
@login_required
def listar_ventas():
    # Filtros GET
    inicio = _parse_date(request.args.get("inicio"))
    fin = _parse_date(request.args.get("fin"))
    consultor = (request.args.get("consultor") or "").strip()
    vista = (request.args.get("vista") or "completa").lower()  # 'completa' | 'compacta'

    q = Venta.query
    if inicio:
        q = q.filter(Venta.fecha >= inicio)
    if fin:
        q = q.filter(Venta.fecha <= fin)
    if consultor:
        q = q.filter(Venta.nombre_consultor.ilike(f"%{consultor}%"))

    ventas = q.order_by(desc(Venta.fecha), desc(Venta.id)).all()
    return render_template("ventas_list.html", ventas=ventas, vista=vista)

@bp.route("/nueva", methods=["GET","POST"])
@login_required
@require_role(["admin","user"])
def nueva_venta():
    form = VentaForm()
    if request.method == "GET":
        form.fecha.data = date.today()
    if form.validate_on_submit():
        v = Venta(
            fecha=form.fecha.data,
            periodo=form.periodo.data,
            sector=form.sector.data,
            nombre_consultor=form.nombre_consultor.data.strip(),
            nombre_cliente=form.nombre_cliente.data.strip(),
            origen_venta=form.origen_venta.data,
            n_cotizacion_odoo=form.n_cotizacion_odoo.data.strip() or None,
            n_licitacion=form.n_licitacion.data.strip() or None,
            tipo_servicio=form.tipo_servicio.data,
            plazo_contrato=form.plazo_contrato.data,
            tipo_venta=form.tipo_venta.data,
            fcv_nuevo=form.fcv_nuevo.data,
            fcv_renovado=form.fcv_renovado.data,
            mrc_inicial=form.mrc_inicial.data,
            pago_unico=form.pago_unico.data,
        )
        v.recompute()
        db.session.add(v)
        db.session.commit()
        flash("Venta registrada correctamente", "success")
        return redirect(url_for("ventas.listar_ventas"))
    return render_template("venta_form.html", form=form, modo="Nueva")

@bp.route("/editar/<int:venta_id>", methods=["GET","POST"])
@login_required
@require_role(["admin","user"])
def editar_venta(venta_id):
    v = Venta.query.get_or_404(venta_id)
    form = VentaForm(obj=v)
    if form.validate_on_submit():
        form.populate_obj(v)
        v.recompute()
        db.session.commit()
        flash("Venta actualizada", "success")
        return redirect(url_for("ventas.listar_ventas"))
    return render_template("venta_form.html", form=form, modo="Editar")

@bp.route("/eliminar/<int:venta_id>", methods=["POST"])
@login_required
@require_role(["admin"])
def eliminar_venta(venta_id):
    v = Venta.query.get_or_404(venta_id)
    db.session.delete(v)
    db.session.commit()
    flash("Venta eliminada", "info")
    return redirect(url_for("ventas.listar_ventas"))
