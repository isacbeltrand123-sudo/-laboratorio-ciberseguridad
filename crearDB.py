
import sqlite3

# Conectar con la base de datos
conexion = sqlite3.connect("usuarios.db")

# Crear cursor
cursor = conexion.cursor()

# Crear tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    correo TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Guardar cambios
conexion.commit()

# Cerrar conexión
conexion.close()

print("Base de datos creada correctamente.")
