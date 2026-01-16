"""
Script para poblar la base de datos con datos aleatorios:
- 16 equipos
- Jugadores para cada equipo (11-15 jugadores por equipo)
- Árbitros
- Partidos de dieciseisavos de final
"""

import sys
import random
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication
from Models.database import conectar
from Models.equipo import Equipo
from Models.participante import Participante
from Models.jugador_equipo import JugadorEquipo
from Models.partido import Partido

# Listas de datos aleatorios
NOMBRES = [
    "Lucas",
    "Martín",
    "Alejandro",
    "Daniel",
    "Pablo",
    "Diego",
    "Javier",
    "Carlos",
    "Miguel",
    "David",
    "Jorge",
    "Sergio",
    "Adrián",
    "Raúl",
    "Fernando",
    "Antonio",
    "Manuel",
    "Francisco",
    "José",
    "Juan",
    "Alberto",
    "Rubén",
    "Iván",
    "Óscar",
    "Eduardo",
    "Ricardo",
    "Rafael",
    "Víctor",
    "Andrés",
    "Gabriel",
    "Marco",
    "Hugo",
]

APELLIDOS = [
    "García",
    "Rodríguez",
    "Martínez",
    "López",
    "González",
    "Pérez",
    "Sánchez",
    "Ramírez",
    "Torres",
    "Flores",
    "Rivera",
    "Gómez",
    "Díaz",
    "Cruz",
    "Morales",
    "Reyes",
    "Hernández",
    "Jiménez",
    "Ruiz",
    "Álvarez",
    "Castillo",
    "Romero",
    "Silva",
    "Ortiz",
    "Vargas",
    "Castro",
    "Vega",
    "Ramos",
    "Muñoz",
    "Navarro",
    "Campos",
    "Santos",
]

# Mapeo de equipos con sus escudos existentes
EQUIPOS_CONFIG = [
    {"nombre": "Real Madrid", "escudo": "spain_real-madrid.football-logos.cc.svg"},
    {"nombre": "FC Barcelona", "escudo": "spain_barcelona.football-logos.cc.svg"},
    {
        "nombre": "Atlético Madrid",
        "escudo": "spain_atletico-madrid.football-logos.cc.svg",
    },
    {"nombre": "Valencia CF", "escudo": "spain_valencia.football-logos.cc.svg"},
    {"nombre": "Sevilla FC", "escudo": "spain_sevilla.football-logos.cc.svg"},
    {
        "nombre": "Athletic Bilbao",
        "escudo": "spain_athletic-club.football-logos.cc.svg",
    },
    {"nombre": "Real Sociedad", "escudo": "spain_real-sociedad.football-logos.cc.svg"},
    {"nombre": "Villarreal CF", "escudo": "spain_villarreal.football-logos.cc.svg"},
    {"nombre": "Real Betis", "escudo": "spain_real-betis.football-logos.cc.svg"},
    {
        "nombre": "Celta de Vigo",
        "escudo": "spain_tenerife.football-logos.cc.svg",
    },  # Usando Tenerife
    {"nombre": "Espanyol", "escudo": "spain_espanyol.football-logos.cc.svg"},
    {
        "nombre": "Getafe CF",
        "escudo": "spain_girona.football-logos.cc.svg",
    },  # Usando Girona
    {
        "nombre": "Levante UD",
        "escudo": "spain_malaga.football-logos.cc.svg",
    },  # Usando Málaga
    {
        "nombre": "Osasuna",
        "escudo": "spain_oviedo.football-logos.cc.svg",
    },  # Usando Oviedo
    {
        "nombre": "Deportivo",
        "escudo": "spain_deportivo-la-coruna.football-logos.cc.svg",
    },
    {
        "nombre": "Mallorca",
        "escudo": "spain_valladolid.football-logos.cc.svg",
    },  # Usando Valladolid
]

CURSOS = ["1DAM", "2DAM", "1DAW", "2DAW", "1ASIR", "2ASIR"]

COLORES = [
    "#FFFFFF",
    "#FF0000",
    "#0000FF",
    "#FFFF00",
    "#00FF00",
    "#FFA500",
    "#800080",
    "#00FFFF",
    "#FF69B4",
    "#808080",
    "#000000",
    "#90EE90",
    "#FFD700",
    "#FF4500",
    "#1E90FF",
    "#32CD32",
]

POSICIONES = ["Portero", "Defensa", "Centrocampista", "Delantero"]


def generar_nombre_completo():
    """Genera un nombre completo aleatorio"""
    return f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"


def generar_fecha_nacimiento():
    """Genera una fecha de nacimiento aleatoria (entre 16 y 25 años)"""
    anos = random.randint(16, 25)
    fecha = datetime.now() - timedelta(days=anos * 365 + random.randint(0, 364))
    return fecha.strftime("%Y-%m-%d")


def crear_equipos():
    """Crea 16 equipos usando los escudos existentes"""
    print("\n=== Creando equipos ===")
    equipos_ids = []

    for i, equipo_config in enumerate(EQUIPOS_CONFIG):
        equipo = Equipo(
            nombre=equipo_config["nombre"],
            curso=random.choice(CURSOS),
            color=COLORES[i],
            escudo=equipo_config["escudo"],
        )
        if equipo.guardar():
            equipos_ids.append(equipo.id)
            print(f"✓ Creado equipo: {equipo_config['nombre']} (ID: {equipo.id})")
        else:
            print(f"✗ Error al crear equipo: {equipo_config['nombre']}")

    return equipos_ids

    return equipos_ids


def crear_jugadores_para_equipo(equipo_id, curso):
    """Crea jugadores para un equipo específico"""
    num_jugadores = random.randint(11, 15)  # Entre 11 y 15 jugadores
    jugadores_creados = []

    # Asegurar al menos un portero
    posiciones = ["Portero"] + [
        random.choice(["Defensa", "Centrocampista", "Delantero"])
        for _ in range(num_jugadores - 1)
    ]
    random.shuffle(posiciones[1:])  # Mantener el portero al principio

    for i in range(num_jugadores):
        participante = Participante(
            nombre=generar_nombre_completo(),
            fecha_nacimiento=generar_fecha_nacimiento(),
            curso=curso,
            es_jugador=True,
            es_arbitro=False,
            posicion=posiciones[i],
        )
        if participante.guardar():
            participante_id = participante.id

            # Asignar jugador al equipo
            jugador_equipo = JugadorEquipo(
                jugador_id=participante_id, equipo_id=equipo_id
            )
            jugador_equipo.guardar()

            jugadores_creados.append(participante_id)

    return jugadores_creados


def crear_todos_los_jugadores(equipos_ids):
    """Crea jugadores para todos los equipos"""
    print("\n=== Creando jugadores ===")

    for equipo_id in equipos_ids:
        # Obtener información del equipo
        from PySide6.QtSql import QSqlQuery

        query = QSqlQuery()
        query.prepare("SELECT nombre, curso FROM equipos WHERE id = ?")
        query.addBindValue(equipo_id)
        query.exec()

        if query.next():
            nombre_equipo = query.value(0)
            curso = query.value(1)
            jugadores = crear_jugadores_para_equipo(equipo_id, curso)
            print(f"✓ Creados {len(jugadores)} jugadores para {nombre_equipo}")


def crear_arbitros():
    """Crea árbitros aleatorios"""
    print("\n=== Creando árbitros ===")
    arbitros_ids = []
    num_arbitros = 10  # Crear 10 árbitros

    for i in range(num_arbitros):
        participante = Participante(
            nombre=generar_nombre_completo(),
            fecha_nacimiento=generar_fecha_nacimiento(),
            curso=random.choice(CURSOS),
            es_jugador=False,
            es_arbitro=True,
            posicion="",
        )
        if participante.guardar():
            arbitro_id = participante.id
            arbitros_ids.append(arbitro_id)
            print(f"✓ Creado árbitro: {participante.nombre} (ID: {arbitro_id})")

    return arbitros_ids


def crear_partidos_dieciseisavos(equipos_ids, arbitros_ids):
    """Crea los partidos de dieciseisavos de final (8 partidos)"""
    print("\n=== Creando partidos de dieciseisavos ===")

    # Mezclar equipos para emparejarlos aleatoriamente
    equipos_mezclados = equipos_ids.copy()
    random.shuffle(equipos_mezclados)

    # Generar fechas para los próximos días
    fecha_base = datetime.now() + timedelta(days=1)

    partidos_creados = []
    for i in range(8):  # 8 partidos (16 equipos / 2)
        equipo_local = equipos_mezclados[i * 2]
        equipo_visitante = equipos_mezclados[i * 2 + 1]
        arbitro = random.choice(arbitros_ids)

        # Distribuir partidos en diferentes días
        fecha_partido = fecha_base + timedelta(days=i // 2, hours=(i % 2) * 2)

        partido = Partido(
            equipo_local_id=equipo_local,
            equipo_visitante_id=equipo_visitante,
            fecha_hora=fecha_partido.strftime("%Y-%m-%d %H:%M:%S"),
            arbitro_id=arbitro,
            eliminatoria="Octavos",
            jugado=False,
        )
        if partido.guardar():
            partido_id = partido.id
            partidos_creados.append(partido_id)

            # Obtener nombres de equipos para mostrar
            from PySide6.QtSql import QSqlQuery

            query = QSqlQuery()
            query.prepare("SELECT nombre FROM equipos WHERE id = ?")
            query.addBindValue(equipo_local)
            query.exec()
            query.next()
            nombre_local = query.value(0)

            query.prepare("SELECT nombre FROM equipos WHERE id = ?")
            query.addBindValue(equipo_visitante)
            query.exec()
            query.next()
            nombre_visitante = query.value(0)

            print(f"✓ Partido {i+1}: {nombre_local} vs {nombre_visitante}")
            print(f"  Fecha: {fecha_partido.strftime('%Y-%m-%d %H:%M')}")

    return partidos_creados


def limpiar_base_datos():
    """Limpia todas las tablas de la base de datos"""
    print("\n=== Limpiando base de datos ===")
    from PySide6.QtSql import QSqlQuery

    query = QSqlQuery()
    tablas = [
        "goles",
        "tarjetas",
        "jugadores_equipos",
        "partidos",
        "participantes",
        "equipos",
    ]

    for tabla in tablas:
        if query.exec(f"DELETE FROM {tabla}"):
            print(f"✓ Tabla {tabla} limpiada")
        else:
            print(f"✗ Error al limpiar tabla {tabla}: {query.lastError().text()}")


def main():
    """Función principal"""
    print("=" * 60)
    print("POBLANDO BASE DE DATOS CON DATOS ALEATORIOS")
    print("=" * 60)

    # Crear aplicación Qt (necesaria para QSqlDatabase)
    app = QApplication(sys.argv)

    # Conectar a la base de datos
    try:
        db = conectar()
        print("✓ Conexión a base de datos establecida")
    except Exception as e:
        print(f"✗ Error al conectar a la base de datos: {e}")
        return

    # Preguntar si limpiar la base de datos
    respuesta = input("\n¿Deseas limpiar la base de datos antes de poblarla? (s/n): ")
    if respuesta.lower() == "s":
        limpiar_base_datos()

    # Crear datos
    equipos_ids = crear_equipos()
    crear_todos_los_jugadores(equipos_ids)
    arbitros_ids = crear_arbitros()
    partidos_ids = crear_partidos_dieciseisavos(equipos_ids, arbitros_ids)

    print("\n" + "=" * 60)
    print("✓ BASE DE DATOS POBLADA EXITOSAMENTE")
    print("=" * 60)
    print(f"Total equipos creados: {len(equipos_ids)}")
    print(f"Total árbitros creados: {len(arbitros_ids)}")
    print(f"Total partidos creados: {len(partidos_ids)}")
    print("\n¡Ya puedes probar la aplicación con datos reales!")


if __name__ == "__main__":
    main()
