
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")

print("Base de datos utilizada:")
print(DB_PATH)

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

cursor.execute("SELECT usuario, correo, LENGTH(password) FROM usuarios")

usuarios = cursor.fetchall()

print("\nUsuarios encontrados:")

if usuarios:
    for usuario in usuarios:
        print("Usuario:", usuario[0])
        print("Correo:", usuario[1])
        print("Longitud del hash:", usuario[2])
        print("-----------------------")
else:
    print("No hay usuarios registrados.")

conexion.close()


