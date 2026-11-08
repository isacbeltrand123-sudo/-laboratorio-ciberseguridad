
import sqlite3
import os
from getpass import getpass
from werkzeug.security import check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")

conexion = sqlite3.connect(DB_PATH)
conexion.row_factory = sqlite3.Row

usuario = input("Escribe tu usuario: ").strip()
password = getpass("Escribe tu contraseña: ")

cursor = conexion.cursor()

cursor.execute(
    "SELECT * FROM usuarios WHERE usuario = ? OR correo = ?",
    (usuario, usuario)
)

datos = cursor.fetchone()

if datos:
    print("\nUsuario encontrado.")

    if check_password_hash(datos["password"], password):
        print("CONTRASEÑA CORRECTA.")
    else:
        print("CONTRASEÑA INCORRECTA.")
else:
    print("\nUsuario no encontrado.")

conexion.close()
