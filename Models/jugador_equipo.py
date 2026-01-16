"""
Modelo de datos para la relación Jugador-Equipo.

Este módulo gestiona la asignación de jugadores a equipos.
"""

from PySide6.QtSql import QSqlQuery
from datetime import datetime


class JugadorEquipo:
    """
    Clase que representa la relación entre un jugador y un equipo.

    Attributes:
        id (int): Identificador único de la relación
        jugador_id (int): ID del jugador
        equipo_id (int): ID del equipo
        fecha_asignacion (str): Fecha de asignación
    """

    def __init__(self, id=None, jugador_id=None, equipo_id=None, fecha_asignacion=""):
        """
        Inicializa un objeto JugadorEquipo.
        """
        self.id = id
        self.jugador_id = jugador_id
        self.equipo_id = equipo_id
        self.fecha_asignacion = fecha_asignacion or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def guardar(self):
        """
        Guarda la relación en la base de datos.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO jugadores_equipos (jugador_id, equipo_id, fecha_asignacion)
            VALUES (?, ?, ?)
        """
        )
        query.addBindValue(self.jugador_id)
        query.addBindValue(self.equipo_id)
        query.addBindValue(self.fecha_asignacion)

        if query.exec():
            self.id = query.lastInsertId()
            return True
        else:
            print(f"Error al asignar jugador a equipo: {query.lastError().text()}")
            return False

    def eliminar(self):
        """
        Elimina la relación de la base de datos.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.id:
            return False

        query = QSqlQuery()
        query.prepare("DELETE FROM jugadores_equipos WHERE id = ?")
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar asignación: {query.lastError().text()}")
            return False

    @staticmethod
    def asignar_jugador(jugador_id, equipo_id):
        """
        Asigna un jugador a un equipo.

        Args:
            jugador_id (int): ID del jugador
            equipo_id (int): ID del equipo

        Returns:
            bool: True si se asignó correctamente, False en caso contrario
        """
        relacion = JugadorEquipo(jugador_id=jugador_id, equipo_id=equipo_id)
        return relacion.guardar()

    @staticmethod
    def desasignar_jugador(jugador_id, equipo_id):
        """
        Desasigna un jugador de un equipo.

        Args:
            jugador_id (int): ID del jugador
            equipo_id (int): ID del equipo

        Returns:
            bool: True si se desasignó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            "DELETE FROM jugadores_equipos WHERE jugador_id = ? AND equipo_id = ?"
        )
        query.addBindValue(jugador_id)
        query.addBindValue(equipo_id)

        if query.exec():
            return True
        else:
            print(f"Error al desasignar jugador: {query.lastError().text()}")
            return False

    @staticmethod
    def obtener_equipo_de_jugador(jugador_id):
        """
        Obtiene el equipo al que pertenece un jugador.

        Args:
            jugador_id (int): ID del jugador

        Returns:
            int: ID del equipo, o None si no tiene equipo
        """
        query = QSqlQuery()
        query.prepare("SELECT equipo_id FROM jugadores_equipos WHERE jugador_id = ?")
        query.addBindValue(jugador_id)

        if query.exec() and query.next():
            return query.value(0)
        return None

    @staticmethod
    def jugador_tiene_equipo(jugador_id):
        """
        Verifica si un jugador ya está asignado a un equipo.

        Args:
            jugador_id (int): ID del jugador

        Returns:
            bool: True si tiene equipo, False en caso contrario
        """
        return JugadorEquipo.obtener_equipo_de_jugador(jugador_id) is not None

    @staticmethod
    def obtener_jugadores_de_equipo(equipo_id):
        """
        Obtiene la lista de IDs de jugadores asignados a un equipo.

        Args:
            equipo_id (int): ID del equipo

        Returns:
            list: Lista de IDs de jugadores del equipo
        """
        jugadores_ids = []
        query = QSqlQuery()
        query.prepare("SELECT jugador_id FROM jugadores_equipos WHERE equipo_id = ?")
        query.addBindValue(equipo_id)

        if query.exec():
            while query.next():
                jugadores_ids.append(query.value(0))

        return jugadores_ids

    @staticmethod
    def contar_jugadores_equipo(equipo_id):
        """
        Cuenta cuántos jugadores tiene un equipo.

        Args:
            equipo_id (int): ID del equipo

        Returns:
            int: Número de jugadores
        """
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM jugadores_equipos WHERE equipo_id = ?")
        query.addBindValue(equipo_id)

        if query.exec() and query.next():
            return query.value(0)
        return 0

    @staticmethod
    def equipo_completo(equipo_id, max_jugadores=18):
        """
        Verifica si un equipo ya alcanzó el máximo de jugadores permitidos.

        Args:
            equipo_id (int): ID del equipo
            max_jugadores (int): Máximo de jugadores permitidos (por defecto 18)

        Returns:
            bool: True si está completo, False si aún puede añadir jugadores
        """
        return JugadorEquipo.contar_jugadores_equipo(equipo_id) >= max_jugadores
