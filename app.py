
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import csv
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_temporal_cambiar_en_produccion"

# Rutas de los archivos
CARPETA = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CARPETA, "usuarios.db")
LOG_PATH = os.path.join(CARPETA, "eventos.log")


def conectar_db():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


# Registrar eventos de seguridad
def registrar_evento(tipo, usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([fecha, tipo, usuario])


@app.route("/")
def inicio():
    return render_template("login.html", mensaje="")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = ""

    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        correo = request.form["correo"].strip()
        password = request.form["password"]

        if not usuario or not correo or not password:
            mensaje = "Todos los campos son obligatorios."

        elif len(password) < 8:
            mensaje = "La contraseña debe tener al menos 8 caracteres."

        else:
            conexion = conectar_db()
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?",
                (usuario, correo)
            )

            existente = cursor.fetchone()

            if existente:
                mensaje = "El usuario o correo ya existe."
            else:
                password_hash = generate_password_hash(password)

                cursor.execute(
                    """INSERT INTO usuarios
                    (usuario, correo, password)
                    VALUES (?, ?, ?)""",
                    (usuario, correo, password_hash)
                )

                conexion.commit()
                mensaje = "Usuario registrado correctamente."

            conexion.close()

    return render_template("registro.html", mensaje=mensaje)


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        password = request.form["password"]

        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        datos = cursor.fetchone()
        conexion.close()

        if datos and check_password_hash(datos["password"], password):
            registrar_evento("LOGIN_CORRECTO", usuario)

            session["usuario"] = datos["usuario"]
            return redirect(url_for("panel"))

        else:
            registrar_evento("LOGIN_FALLIDO", usuario)
            mensaje = "Usuario o contraseña incorrectos."

    return render_template("login.html", mensaje=mensaje)


@app.route("/panel")
def panel():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("panel.html")


@app.route("/usuarios")
def usuarios():
    if "usuario" not in session:
        return redirect(url_for("login"))

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, usuario, correo FROM usuarios ORDER BY id DESC"
    )

    lista_usuarios = cursor.fetchall()
    conexion.close()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
