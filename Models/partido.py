"""
Modelo de datos para la entidad Partido.

Este módulo contiene la clase Partido con todos los métodos CRUD
y operaciones relacionadas con la gestión de partidos.
"""

from PySide6.QtSql import QSqlQuery
from datetime import datetime
import csv


class Partido:
    """
    Clase que representa un partido en el torneo.

    Attributes:
        id (int): Identificador único del partido
        equipo_local_id (int): ID del equipo local
        equipo_visitante_id (int): ID del equipo visitante
        fecha_hora (str): Fecha y hora del partido
        arbitro_id (int): ID del árbitro asignado
        eliminatoria (str): Fase del torneo
        goles_local (int): Goles del equipo local
        goles_visitante (int): Goles del equipo visitante
        jugado (bool): Indica si el partido ya se jugó
        ganador_id (int): ID del equipo ganador
        prorroga (bool): Indica si hubo prórroga
        penales_local (int): Goles en penales del equipo local
        penales_visitante (int): Goles en penales del equipo visitante
    """

    ELIMINATORIAS = [
        "Octavos",
        "Cuartos",
        "Semifinales",
        "Final",
    ]

    def __init__(
        self,
        id=None,
        equipo_local_id=None,
        equipo_visitante_id=None,
        fecha_hora="",
        arbitro_id=None,
        eliminatoria="Octavos",
        goles_local=0,
        goles_visitante=0,
        jugado=False,
        ganador_id=None,
        prorroga=False,
        penales_local=None,
        penales_visitante=None,
    ):
        """
        Inicializa un objeto Partido.
        """
        self.id = id
        self.equipo_local_id = equipo_local_id
        self.equipo_visitante_id = equipo_visitante_id
        self.fecha_hora = fecha_hora
        self.arbitro_id = arbitro_id
        self.eliminatoria = eliminatoria
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante
        self.jugado = jugado
        self.ganador_id = ganador_id
        self.prorroga = prorroga
        self.penales_local = penales_local
        self.penales_visitante = penales_visitante

    def guardar(self):
        """
        Guarda el partido en la base de datos.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if self.id:
            return self.actualizar()
        else:
            return self.crear()

    def crear(self):
        """
        Inserta un nuevo partido en la base de datos.

        Returns:
            bool: True si se insertó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO partidos 
            (equipo_local_id, equipo_visitante_id, fecha_hora, arbitro_id, eliminatoria,
             goles_local, goles_visitante, jugado, ganador_id, prorroga, penales_local, penales_visitante)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        )
        query.addBindValue(self.equipo_local_id)
        query.addBindValue(self.equipo_visitante_id)
        query.addBindValue(self.fecha_hora)
        query.addBindValue(self.arbitro_id)
        query.addBindValue(self.eliminatoria)
        query.addBindValue(self.goles_local)
        query.addBindValue(self.goles_visitante)
        query.addBindValue(1 if self.jugado else 0)
        query.addBindValue(self.ganador_id)
        query.addBindValue(1 if self.prorroga else 0)
        query.addBindValue(self.penales_local)
        query.addBindValue(self.penales_visitante)

        if query.exec():
            self.id = query.lastInsertId()
            return True
        else:
            print(f"Error al crear partido: {query.lastError().text()}")
            return False

    def actualizar(self):
        """
        Actualiza los datos del partido en la base de datos.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            UPDATE partidos 
            SET equipo_local_id = ?, equipo_visitante_id = ?, fecha_hora = ?, 
                arbitro_id = ?, eliminatoria = ?, goles_local = ?, goles_visitante = ?,
                jugado = ?, ganador_id = ?, prorroga = ?, penales_local = ?, penales_visitante = ?
            WHERE id = ?
        """
        )
        query.addBindValue(self.equipo_local_id)
        query.addBindValue(self.equipo_visitante_id)
        query.addBindValue(self.fecha_hora)
        query.addBindValue(self.arbitro_id)
        query.addBindValue(self.eliminatoria)
        query.addBindValue(self.goles_local)
        query.addBindValue(self.goles_visitante)
        query.addBindValue(1 if self.jugado else 0)
        query.addBindValue(self.ganador_id)
        query.addBindValue(1 if self.prorroga else 0)
        query.addBindValue(self.penales_local)
        query.addBindValue(self.penales_visitante)
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al actualizar partido: {query.lastError().text()}")
            return False

    def eliminar(self):
        """
        Elimina el partido de la base de datos.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.id:
            return False

        query = QSqlQuery()
        query.prepare("DELETE FROM partidos WHERE id = ?")
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar partido: {query.lastError().text()}")
            return False

    @staticmethod
    def obtener_por_id(partido_id):
        """
        Obtiene un partido por su ID.

        Args:
            partido_id (int): ID del partido a buscar

        Returns:
            Partido: Objeto Partido si se encuentra, None en caso contrario
        """
        query = QSqlQuery()
        query.prepare("SELECT * FROM partidos WHERE id = ?")
        query.addBindValue(partido_id)

        if query.exec() and query.next():
            return Partido(
                id=query.value(0),
                equipo_local_id=query.value(1),
                equipo_visitante_id=query.value(2),
                fecha_hora=query.value(3),
                arbitro_id=query.value(4),
                eliminatoria=query.value(5),
                goles_local=query.value(6),
                goles_visitante=query.value(7),
                jugado=bool(query.value(8)),
                ganador_id=query.value(9),
                prorroga=bool(query.value(10)),
                penales_local=query.value(11),
                penales_visitante=query.value(12),
            )
        return None

    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los partidos de la base de datos ordenados por fecha.

        Returns:
            list: Lista de objetos Partido
        """
        partidos = []
        query = QSqlQuery("SELECT * FROM partidos ORDER BY fecha_hora")

        while query.next():
            partidos.append(
                Partido(
                    id=query.value(0),
                    equipo_local_id=query.value(1),
                    equipo_visitante_id=query.value(2),
                    fecha_hora=query.value(3),
                    arbitro_id=query.value(4),
                    eliminatoria=query.value(5),
                    goles_local=query.value(6),
                    goles_visitante=query.value(7),
                    jugado=bool(query.value(8)),
                    ganador_id=query.value(9),
                    prorroga=bool(query.value(10)),
                    penales_local=query.value(11),
                    penales_visitante=query.value(12),
                )
            )

        return partidos

    @staticmethod
    def obtener_por_eliminatoria(eliminatoria):
        """
        Obtiene todos los partidos de una eliminatoria específica.

        Args:
            eliminatoria (str): Nombre de la eliminatoria

        Returns:
            list: Lista de objetos Partido
        """
        partidos = []
        query = QSqlQuery()
        query.prepare(
            "SELECT * FROM partidos WHERE eliminatoria = ? ORDER BY fecha_hora"
        )
        query.addBindValue(eliminatoria)

        if query.exec():
            while query.next():
                partidos.append(
                    Partido(
                        id=query.value(0),
                        equipo_local_id=query.value(1),
                        equipo_visitante_id=query.value(2),
                        fecha_hora=query.value(3),
                        arbitro_id=query.value(4),
                        eliminatoria=query.value(5),
                        goles_local=query.value(6),
                        goles_visitante=query.value(7),
                        jugado=bool(query.value(8)),
                        ganador_id=query.value(9),
                        prorroga=bool(query.value(10)),
                        penales_local=query.value(11),
                        penales_visitante=query.value(12),
                    )
                )

        return partidos

    @staticmethod
    def obtener_partidos_jugados():
        """
        Obtiene todos los partidos que ya se han jugado.

        Returns:
            list: Lista de objetos Partido jugados
        """
        partidos = []
        query = QSqlQuery(
            "SELECT * FROM partidos WHERE jugado = 1 ORDER BY fecha_hora DESC"
        )

        while query.next():
            partidos.append(
                Partido(
                    id=query.value(0),
                    equipo_local_id=query.value(1),
                    equipo_visitante_id=query.value(2),
                    fecha_hora=query.value(3),
                    arbitro_id=query.value(4),
                    eliminatoria=query.value(5),
                    goles_local=query.value(6),
                    goles_visitante=query.value(7),
                    jugado=bool(query.value(8)),
                    ganador_id=query.value(9),
                    prorroga=bool(query.value(10)),
                    penales_local=query.value(11),
                    penales_visitante=query.value(12),
                )
            )

        return partidos

    @staticmethod
    def obtener_partidos_pendientes():
        """
        Obtiene todos los partidos que aún no se han jugado.

        Returns:
            list: Lista de objetos Partido pendientes
        """
        partidos = []
        query = QSqlQuery("SELECT * FROM partidos WHERE jugado = 0 ORDER BY fecha_hora")

        while query.next():
            partidos.append(
                Partido(
                    id=query.value(0),
                    equipo_local_id=query.value(1),
                    equipo_visitante_id=query.value(2),
                    fecha_hora=query.value(3),
                    arbitro_id=query.value(4),
                    eliminatoria=query.value(5),
                    goles_local=query.value(6),
                    goles_visitante=query.value(7),
                    jugado=bool(query.value(8)),
                    ganador_id=query.value(9),
                    prorroga=bool(query.value(10)),
                    penales_local=query.value(11),
                    penales_visitante=query.value(12),
                )
            )

        return partidos

    @staticmethod
    def obtener_partidos_sin_arbitro():
        """
        Obtiene todos los partidos que no tienen árbitro asignado.

        Returns:
            list: Lista de objetos Partido sin árbitro
        """
        partidos = []
        query = QSqlQuery(
            "SELECT * FROM partidos WHERE arbitro_id IS NULL ORDER BY fecha_hora"
        )

        while query.next():
            partidos.append(
                Partido(
                    id=query.value(0),
                    equipo_local_id=query.value(1),
                    equipo_visitante_id=query.value(2),
                    fecha_hora=query.value(3),
                    arbitro_id=query.value(4),
                    eliminatoria=query.value(5),
                    goles_local=query.value(6),
                    goles_visitante=query.value(7),
                    jugado=bool(query.value(8)),
                    ganador_id=query.value(9),
                    prorroga=bool(query.value(10)),
                    penales_local=query.value(11),
                    penales_visitante=query.value(12),
                )
            )

        return partidos

    @staticmethod
    def obtener_por_fecha(fecha):
        """
        Obtiene todos los partidos de una fecha específica.

        Args:
            fecha (str): Fecha en formato YYYY-MM-DD

        Returns:
            list: Lista de objetos Partido de esa fecha
        """
        partidos = []
        query = QSqlQuery()
        query.prepare(
            "SELECT * FROM partidos WHERE DATE(fecha_hora) = ? ORDER BY fecha_hora"
        )
        query.addBindValue(fecha)

        if query.exec():
            while query.next():
                partidos.append(
                    Partido(
                        id=query.value(0),
                        equipo_local_id=query.value(1),
                        equipo_visitante_id=query.value(2),
                        fecha_hora=query.value(3),
                        arbitro_id=query.value(4),
                        eliminatoria=query.value(5),
                        goles_local=query.value(6),
                        goles_visitante=query.value(7),
                        jugado=bool(query.value(8)),
                        ganador_id=query.value(9),
                        prorroga=bool(query.value(10)),
                        penales_local=query.value(11),
                        penales_visitante=query.value(12),
                    )
                )

        return partidos

    def obtener_nombres_equipos(self):
        """
        Obtiene los nombres de los equipos del partido.

        Returns:
            dict: Diccionario con 'local' y 'visitante'
        """
        query = QSqlQuery()
        query.prepare("SELECT nombre FROM equipos WHERE id = ?")

        query.addBindValue(self.equipo_local_id)
        query.exec()
        nombre_local = query.value(0) if query.next() else "Desconocido"

        query.addBindValue(self.equipo_visitante_id)
        query.exec()
        nombre_visitante = query.value(0) if query.next() else "Desconocido"

        return {"local": nombre_local, "visitante": nombre_visitante}

    @staticmethod
    def exportar_clasificacion_csv(ruta_archivo):
        """
        Exporta la clasificación del torneo (bracket) a un archivo CSV organizado por eliminatoria.

        Args:
            ruta_archivo (str): Ruta donde guardar el archivo CSV

        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        try:
            partidos = Partido.obtener_todos()

            # Organizar partidos por eliminatoria
            partidos_por_fase = {
                "Octavos": [],
                "Cuartos": [],
                "Semifinales": [],
                "Final": [],
            }

            for partido in partidos:
                if partido.eliminatoria in partidos_por_fase:
                    partidos_por_fase[partido.eliminatoria].append(partido)

            with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    [
                        "Eliminatoria",
                        "Equipo Local",
                        "Goles Local",
                        "Equipo Visitante",
                        "Goles Visitante",
                        "Ganador",
                        "Estado",
                    ]
                )

                # Escribir partidos por fase en orden
                for fase in ["Octavos", "Cuartos", "Semifinales", "Final"]:
                    for partido in partidos_por_fase[fase]:
                        # Obtener nombres de equipos
                        query = QSqlQuery()
                        query.prepare("SELECT nombre FROM equipos WHERE id = ?")

                        query.addBindValue(partido.equipo_local_id)
                        query.exec()
                        nombre_local = query.value(0) if query.next() else "—"

                        query.addBindValue(partido.equipo_visitante_id)
                        query.exec()
                        nombre_visitante = query.value(0) if query.next() else "—"

                        # Determinar ganador
                        if partido.ganador_id:
                            query.prepare("SELECT nombre FROM equipos WHERE id = ?")
                            query.addBindValue(partido.ganador_id)
                            query.exec()
                            nombre_ganador = query.value(0) if query.next() else ""
                        else:
                            nombre_ganador = "Empate" if partido.jugado else "Pendiente"

                        # Determinar estado
                        estado = "Jugado" if partido.jugado else "Pendiente"

                        escritor.writerow(
                            [
                                fase,
                                nombre_local,
                                partido.goles_local if partido.jugado else "-",
                                nombre_visitante,
                                partido.goles_visitante if partido.jugado else "-",
                                nombre_ganador,
                                estado,
                            ]
                        )

            return True
        except Exception as e:
            print(f"Error al exportar clasificación a CSV: {e}")
            return False

    @staticmethod
    def exportar_csv(ruta_archivo):
        """
        Exporta todos los partidos a un archivo CSV.

        Args:
            ruta_archivo (str): Ruta donde guardar el archivo CSV

        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        try:
            partidos = Partido.obtener_todos()

            with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    [
                        "ID",
                        "Equipo Local",
                        "Equipo Visitante",
                        "Fecha/Hora",
                        "Árbitro",
                        "Eliminatoria",
                        "Goles Local",
                        "Goles Visitante",
                        "Jugado",
                        "Ganador",
                        "Prórroga",
                        "Penales Local",
                        "Penales Visitante",
                    ]
                )

                for partido in partidos:
                    # Obtener nombres
                    query = QSqlQuery()
                    query.prepare("SELECT nombre FROM equipos WHERE id = ?")

                    query.addBindValue(partido.equipo_local_id)
                    query.exec()
                    nombre_local = query.value(0) if query.next() else ""

                    query.addBindValue(partido.equipo_visitante_id)
                    query.exec()
                    nombre_visitante = query.value(0) if query.next() else ""

                    if partido.arbitro_id:
                        query.prepare("SELECT nombre FROM participantes WHERE id = ?")
                        query.addBindValue(partido.arbitro_id)
                        query.exec()
                        nombre_arbitro = query.value(0) if query.next() else ""
                    else:
                        nombre_arbitro = "Sin asignar"

                    if partido.ganador_id:
                        query.prepare("SELECT nombre FROM equipos WHERE id = ?")
                        query.addBindValue(partido.ganador_id)
                        query.exec()
                        nombre_ganador = query.value(0) if query.next() else ""
                    else:
                        nombre_ganador = "Empate" if partido.jugado else "Pendiente"

                    escritor.writerow(
                        [
                            partido.id,
                            nombre_local,
                            nombre_visitante,
                            partido.fecha_hora,
                            nombre_arbitro,
                            partido.eliminatoria,
                            partido.goles_local,
                            partido.goles_visitante,
                            "Sí" if partido.jugado else "No",
                            nombre_ganador,
                            "Sí" if partido.prorroga else "No",
                            partido.penales_local or "",
                            partido.penales_visitante or "",
                        ]
                    )

            return True
        except Exception as e:
            print(f"Error al exportar partidos a CSV: {e}")
            return False

    def __str__(self):
        """
        Representación en string del partido.

        Returns:
            str: Descripción básica del partido
        """
        nombres = self.obtener_nombres_equipos()
        return f"{nombres['local']} vs {nombres['visitante']}"

    def __repr__(self):
        """
        Representación técnica del partido.

        Returns:
            str: Representación con atributos principales
        """
        return f"Partido(id={self.id}, eliminatoria='{self.eliminatoria}', fecha='{self.fecha_hora}')"
