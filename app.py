import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# -----------------------
# Crear app Flask
# -----------------------
app = Flask(__name__)

# 🔥 CONEXIÓN A POSTGRESQL (Render)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://crud_alumnos_2026_user:1calS9AaCgbDv8Lms5Jzfo4PMNFQVvrn@dpg-d6ai0kfgi27c73b7ibeg-a.oregon-postgres.render.com/crud_alumnos_2026"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# Modelo
# -----------------------
class Receta(db.Model):
    __tablename__ = 'recetas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(60))
    tiempo_min = db.Column(db.Integer, default=0)
    porciones = db.Column(db.Integer, default=0)
    ingredientes = db.Column(db.Text)
    instrucciones = db.Column(db.Text)

# -----------------------
# Crear tablas si no existen
# -----------------------
with app.app_context():
    db.create_all()

# -----------------------
# Evitar caché del navegador
# -----------------------
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# -----------------------
# RUTA PRINCIPAL
# -----------------------
@app.route("/")
def home():
    recetas = Receta.query.order_by(Receta.id.desc()).all()
    return render_template("index.html", recetas=recetas)

# -----------------------
# CREAR RECETA
# -----------------------
@app.route("/recetas/nueva", methods=["GET", "POST"])
def nueva_receta():
    if request.method == "POST":
        receta = Receta(
            titulo=request.form["titulo"].strip(),
            categoria=request.form.get("categoria", "").strip(),
            tiempo_min=int(request.form.get("tiempo_min") or 0),
            porciones=int(request.form.get("porciones") or 0),
            ingredientes=request.form.get("ingredientes", "").strip(),
            instrucciones=request.form.get("instrucciones", "").strip(),
        )
        db.session.add(receta)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("nueva_receta.html")

# -----------------------
# VER RECETA  ✅
# -----------------------
@app.route("/recetas/<int:id>")
def ver_receta(id):
    receta = Receta.query.get_or_404(id)
    return render_template("ver_receta.html", receta=receta)

# -----------------------
# EDITAR RECETA
# -----------------------
@app.route("/recetas/<int:id>/editar", methods=["GET", "POST"])
def editar_receta(id):
    receta = Receta.query.get_or_404(id)

    if request.method == "POST":
        receta.titulo = request.form["titulo"].strip()
        receta.categoria = request.form.get("categoria", "").strip()
        receta.tiempo_min = int(request.form.get("tiempo_min") or 0)
        receta.porciones = int(request.form.get("porciones") or 0)
        receta.ingredientes = request.form.get("ingredientes", "").strip()
        receta.instrucciones = request.form.get("instrucciones", "").strip()

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("editar_receta.html", receta=receta)

# -----------------------
# ELIMINAR RECETA
# -----------------------
@app.route("/recetas/<int:id>/eliminar", methods=["POST"])
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    return redirect(url_for("home"))

# -----------------------
# Ejecutar app
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)