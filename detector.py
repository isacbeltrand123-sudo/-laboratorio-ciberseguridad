
import csv
import os
import time
from datetime import datetime

CARPETA = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(CARPETA, "eventos.log")
RESPUESTA_PATH = os.path.join(CARPETA, "respuesta.log")


def detectar_ataques():
    if not os.path.exists(LOG_PATH):
        print("No existe el archivo eventos.log.")
        return

    intentos = {}

    with open(LOG_PATH, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)

        for fila in lector:
            if len(fila) != 3:
                continue

            fecha, tipo, usuario = fila

            if tipo == "LOGIN_FALLIDO":
                if usuario not in intentos:
                    intentos[usuario] = []

                intentos[usuario].append(fecha)

            elif tipo == "LOGIN_CORRECTO":
                intentos[usuario] = []

    encontrado = False

    for usuario, fallos in intentos.items():
        if len(fallos) >= 3:
            encontrado = True

            primer_intento = datetime.strptime(
                fallos[0], "%Y-%m-%d %H:%M:%S"
            )

            deteccion = datetime.now()
            mttd = (deteccion - primer_intento).total_seconds()

            print("\n¡ALERTA DE SEGURIDAD!")
            print("Usuario:", usuario)
            print("Intentos fallidos:", len(fallos))
            print("Hora de detección:", deteccion.strftime("%Y-%m-%d %H:%M:%S"))
            print("MTTD:", round(mttd, 2), "segundos")

            # Simular el tiempo de respuesta
            time.sleep(2)

            respuesta = datetime.now()
            mttr = (respuesta - deteccion).total_seconds()

            # Registrar el bloqueo simulado
            with open(RESPUESTA_PATH, "a", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([
                    respuesta.strftime("%Y-%m-%d %H:%M:%S"),
                    "USUARIO_BLOQUEADO",
                    usuario
                ])

            print("\n¡RESPUESTA AL INCIDENTE!")
            print("Acción: Usuario bloqueado (simulación)")
            print("Hora de respuesta:", respuesta.strftime("%Y-%m-%d %H:%M:%S"))
            print("MTTR:", round(mttr, 2), "segundos")

    if not encontrado:
        print("No se detectaron usuarios con 3 o más intentos fallidos.")


if __name__ == "__main__":
    detectar_ataques()
