"""
Módulo de gestión de base de datos SQLite para el sistema de gestión de torneo de fútbol.

Este módulo maneja la conexión a la base de datos, creación de tablas,
activación de foreign keys y configuración de triggers para mantener
la integridad de los datos.
"""

from PySide6.QtSql import QSqlDatabase, QSqlQuery
import sys
import os
import shutil


def obtener_ruta_bd():
    """
    Obtiene la ruta absoluta de la base de datos.
    Compatible con PyInstaller para el ejecutable.

    En modo ejecutable, copia la BD incluida al directorio del .exe
    para permitir persistencia de datos.

    Returns:
        str: Ruta absoluta al archivo de base de datos
    """
    if getattr(sys, "frozen", False):
        # Ejecutando como ejecutable empaquetado
        # La BD incluida está en sys._MEIPASS (solo lectura)
        bd_origen = os.path.join(sys._MEIPASS, "Models", "torneoFutbol_sqlite.db")

        # La BD de trabajo estará junto al .exe (lectura/escritura)
        directorio_exe = os.path.dirname(sys.executable)
        bd_destino = os.path.join(directorio_exe, "torneoFutbol_sqlite.db")

        # Si no existe la BD junto al exe, copiarla desde el paquete
        if not os.path.exists(bd_destino):
            print(f"Copiando base de datos inicial a {bd_destino}")
            shutil.copy2(bd_origen, bd_destino)

        return bd_destino
    else:
        # Ejecutando en modo desarrollo
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(ruta_base, "torneoFutbol_sqlite.db")


def conectar():
    """
    Establece la conexión con la base de datos SQLite y configura el entorno.

    Realiza las siguientes operaciones:
    - Crea la conexión con el driver QSQLITE
    - Abre la base de datos (la crea si no existe)
    - Activa las foreign keys
    - Crea todas las tablas necesarias
    - Configura los triggers
    - Crea índices para optimización

    Returns:
        QSqlDatabase: Objeto de conexión a la base de datos

    Raises:
        Exception: Si no se puede abrir la base de datos
    """
    db = QSqlDatabase.addDatabase("QSQLITE")
    ruta_bd = obtener_ruta_bd()
    db.setDatabaseName(ruta_bd)

    if not db.open():
        raise Exception(f"No se pudo abrir la base de datos: {db.lastError().text()}")

    print(f"Base de datos conectada correctamente: {ruta_bd}")

    query = QSqlQuery()

    # Activar foreign keys (SQLite las desactiva por defecto)
    if not query.exec("PRAGMA foreign_keys = ON;"):
        print(f"Error al activar foreign keys: {query.lastError().text()}")
    else:
        print("Foreign keys activadas correctamente")

    # Crear todas las tablas
    crear_tablas(query)

    # Crear triggers
    crear_triggers(query)

    # Crear índices
    crear_indices(query)

    return db


def crear_tablas(query):
    """
    Crea todas las tablas necesarias para el sistema si no existen.

    Tablas creadas:
    - equipos: Información de los equipos
    - participantes: Jugadores y árbitros
    - jugadores_equipos: Relación N:M entre jugadores y equipos
    - partidos: Información de los partidos programados
    - goles: Registro de goles por jugador en cada partido
    - tarjetas: Registro de tarjetas amarillas y rojas
    - configuracion: Parámetros de configuración del sistema

    Args:
        query (QSqlQuery): Objeto query para ejecutar sentencias SQL
    """

    # Tabla de equipos
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            curso TEXT NOT NULL,
            color TEXT NOT NULL,
            escudo TEXT NOT NULL UNIQUE,
            fecha_creacion TEXT NOT NULL
        )
    """
    ):
        print(f"Error al crear tabla equipos: {query.lastError().text()}")
    else:
        print("Tabla 'equipos' verificada/creada correctamente")

    # Tabla de participantes (jugadores y árbitros)
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL,
            curso TEXT NOT NULL,
            es_jugador INTEGER DEFAULT 0,
            es_arbitro INTEGER DEFAULT 0,
            posicion TEXT,
            t_amarillas INTEGER DEFAULT 0,
            t_rojas INTEGER DEFAULT 0,
            goles INTEGER DEFAULT 0
        )
    """
    ):
        print(f"Error al crear tabla participantes: {query.lastError().text()}")
    else:
        print("Tabla 'participantes' verificada/creada correctamente")

    # Tabla de relación jugadores-equipos
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS jugadores_equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador_id INTEGER NOT NULL,
            equipo_id INTEGER NOT NULL,
            fecha_asignacion TEXT NOT NULL,
            FOREIGN KEY (jugador_id) REFERENCES participantes(id) ON DELETE CASCADE,
            FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE CASCADE,
            UNIQUE(jugador_id, equipo_id)
        )
    """
    ):
        print(f"Error al crear tabla jugadores_equipos: {query.lastError().text()}")
    else:
        print("Tabla 'jugadores_equipos' verificada/creada correctamente")

    # Tabla de partidos
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_local_id INTEGER NOT NULL,
            equipo_visitante_id INTEGER NOT NULL,
            fecha_hora TEXT NOT NULL,
            arbitro_id INTEGER,
            eliminatoria TEXT NOT NULL,
            goles_local INTEGER DEFAULT 0,
            goles_visitante INTEGER DEFAULT 0,
            jugado INTEGER DEFAULT 0,
            ganador_id INTEGER,
            prorroga INTEGER DEFAULT 0,
            penales_local INTEGER,
            penales_visitante INTEGER,
            FOREIGN KEY (equipo_local_id) REFERENCES equipos(id) ON DELETE CASCADE,
            FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id) ON DELETE CASCADE,
            FOREIGN KEY (arbitro_id) REFERENCES participantes(id) ON DELETE SET NULL,
            FOREIGN KEY (ganador_id) REFERENCES equipos(id) ON DELETE SET NULL,
            CHECK (equipo_local_id != equipo_visitante_id)
        )
    """
    ):
        print(f"Error al crear tabla partidos: {query.lastError().text()}")
    else:
        print("Tabla 'partidos' verificada/creada correctamente")

    # Tabla de goles
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS goles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partido_id INTEGER NOT NULL,
            jugador_id INTEGER NOT NULL,
            minuto INTEGER,
            FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
            FOREIGN KEY (jugador_id) REFERENCES participantes(id) ON DELETE CASCADE
        )
    """
    ):
        print(f"Error al crear tabla goles: {query.lastError().text()}")
    else:
        print("Tabla 'goles' verificada/creada correctamente")

    # Tabla de tarjetas
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS tarjetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partido_id INTEGER NOT NULL,
            jugador_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            minuto INTEGER,
            FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
            FOREIGN KEY (jugador_id) REFERENCES participantes(id) ON DELETE CASCADE,
            CHECK (tipo IN ('amarilla', 'roja'))
        )
    """
    ):
        print(f"Error al crear tabla tarjetas: {query.lastError().text()}")
    else:
        print("Tabla 'tarjetas' verificada/creada correctamente")

    # Tabla de configuración
    if not query.exec(
        """
        CREATE TABLE IF NOT EXISTS configuracion (
            clave TEXT PRIMARY KEY,
            valor TEXT NOT NULL
        )
    """
    ):
        print(f"Error al crear tabla configuracion: {query.lastError().text()}")
    else:
        print("Tabla 'configuracion' verificada/creada correctamente")

    # Insertar valores de configuración por defecto si no existen
    query.prepare("INSERT OR IGNORE INTO configuracion (clave, valor) VALUES (?, ?)")

    configuraciones = [
        ("max_jugadores_equipo", "18"),
        ("version", "1.0"),
        ("fecha_actualizacion", "2026-01-08"),
    ]

    for clave, valor in configuraciones:
        query.addBindValue(clave)
        query.addBindValue(valor)
        query.exec()


def crear_triggers(query):
    """
    Crea triggers para mantener la integridad y actualización automática de datos.

    Triggers creados:
    - Actualizar contador de goles en participantes al insertar gol
    - Actualizar contador de tarjetas amarillas
    - Actualizar contador de tarjetas rojas
    - Actualizar totales de goles en partido

    Args:
        query (QSqlQuery): Objeto query para ejecutar sentencias SQL
    """

    # Trigger: Actualizar goles del participante al insertar un gol
    query.exec("DROP TRIGGER IF EXISTS actualizar_goles_participante")
    if not query.exec(
        """
        CREATE TRIGGER actualizar_goles_participante
        AFTER INSERT ON goles
        BEGIN
            UPDATE participantes 
            SET goles = goles + 1 
            WHERE id = NEW.jugador_id;
        END;
    """
    ):
        print(
            f"Error al crear trigger actualizar_goles_participante: {query.lastError().text()}"
        )
    else:
        print("Trigger 'actualizar_goles_participante' creado correctamente")

    # Trigger: Actualizar tarjetas amarillas
    query.exec("DROP TRIGGER IF EXISTS actualizar_t_amarillas")
    if not query.exec(
        """
        CREATE TRIGGER actualizar_t_amarillas
        AFTER INSERT ON tarjetas
        WHEN NEW.tipo = 'amarilla'
        BEGIN
            UPDATE participantes 
            SET t_amarillas = t_amarillas + 1 
            WHERE id = NEW.jugador_id;
        END;
    """
    ):
        print(
            f"Error al crear trigger actualizar_t_amarillas: {query.lastError().text()}"
        )
    else:
        print("Trigger 'actualizar_t_amarillas' creado correctamente")

    # Trigger: Actualizar tarjetas rojas
    query.exec("DROP TRIGGER IF EXISTS actualizar_t_rojas")
    if not query.exec(
        """
        CREATE TRIGGER actualizar_t_rojas
        AFTER INSERT ON tarjetas
        WHEN NEW.tipo = 'roja'
        BEGIN
            UPDATE participantes 
            SET t_rojas = t_rojas + 1 
            WHERE id = NEW.jugador_id;
        END;
    """
    ):
        print(f"Error al crear trigger actualizar_t_rojas: {query.lastError().text()}")
    else:
        print("Trigger 'actualizar_t_rojas' creado correctamente")

    # Trigger: Decrementar goles al eliminar
    query.exec("DROP TRIGGER IF EXISTS decrementar_goles_participante")
    if not query.exec(
        """
        CREATE TRIGGER decrementar_goles_participante
        AFTER DELETE ON goles
        BEGIN
            UPDATE participantes 
            SET goles = goles - 1 
            WHERE id = OLD.jugador_id AND goles > 0;
        END;
    """
    ):
        print(
            f"Error al crear trigger decrementar_goles_participante: {query.lastError().text()}"
        )
    else:
        print("Trigger 'decrementar_goles_participante' creado correctamente")

    # Trigger: Decrementar tarjetas amarillas al eliminar
    query.exec("DROP TRIGGER IF EXISTS decrementar_t_amarillas")
    if not query.exec(
        """
        CREATE TRIGGER decrementar_t_amarillas
        AFTER DELETE ON tarjetas
        WHEN OLD.tipo = 'amarilla'
        BEGIN
            UPDATE participantes 
            SET t_amarillas = t_amarillas - 1 
            WHERE id = OLD.jugador_id AND t_amarillas > 0;
        END;
    """
    ):
        print(
            f"Error al crear trigger decrementar_t_amarillas: {query.lastError().text()}"
        )
    else:
        print("Trigger 'decrementar_t_amarillas' creado correctamente")

    # Trigger: Decrementar tarjetas rojas al eliminar
    query.exec("DROP TRIGGER IF EXISTS decrementar_t_rojas")
    if not query.exec(
        """
        CREATE TRIGGER decrementar_t_rojas
        AFTER DELETE ON tarjetas
        WHEN OLD.tipo = 'roja'
        BEGIN
            UPDATE participantes 
            SET t_rojas = t_rojas - 1 
            WHERE id = OLD.jugador_id AND t_rojas > 0;
        END;
    """
    ):
        print(f"Error al crear trigger decrementar_t_rojas: {query.lastError().text()}")
    else:
        print("Trigger 'decrementar_t_rojas' creado correctamente")


def crear_indices(query):
    """
    Crea índices para optimizar las consultas frecuentes.

    Args:
        query (QSqlQuery): Objeto query para ejecutar sentencias SQL
    """

    indices = [
        "CREATE INDEX IF NOT EXISTS idx_jugadores_equipos_jugador ON jugadores_equipos(jugador_id)",
        "CREATE INDEX IF NOT EXISTS idx_jugadores_equipos_equipo ON jugadores_equipos(equipo_id)",
        "CREATE INDEX IF NOT EXISTS idx_partidos_fecha ON partidos(fecha_hora)",
        "CREATE INDEX IF NOT EXISTS idx_partidos_eliminatoria ON partidos(eliminatoria)",
        "CREATE INDEX IF NOT EXISTS idx_goles_partido ON goles(partido_id)",
        "CREATE INDEX IF NOT EXISTS idx_goles_jugador ON goles(jugador_id)",
        "CREATE INDEX IF NOT EXISTS idx_tarjetas_partido ON tarjetas(partido_id)",
        "CREATE INDEX IF NOT EXISTS idx_tarjetas_jugador ON tarjetas(jugador_id)",
    ]

    for indice_sql in indices:
        if not query.exec(indice_sql):
            print(f"Error al crear índice: {query.lastError().text()}")
        else:
            nombre_indice = (
                indice_sql.split("idx_")[1].split(" ")[0]
                if "idx_" in indice_sql
                else "índice"
            )
            print(f"Índice 'idx_{nombre_indice}' creado correctamente")


def cerrar_conexion():
    """
    Cierra la conexión a la base de datos de forma segura.
    """
    db = QSqlDatabase.database()
    if db.isOpen():
        db.close()
        print("Conexión a la base de datos cerrada correctamente")


def verificar_conexion():
    """
    Verifica si la conexión a la base de datos está activa.

    Returns:
        bool: True si la conexión está activa, False en caso contrario
    """
    db = QSqlDatabase.database()
    return db.isOpen()
