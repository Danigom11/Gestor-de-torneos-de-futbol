"""
Modelo de datos para la entidad Gol.

Este módulo gestiona el registro de goles en los partidos.
"""

from PySide6.QtSql import QSqlQuery


class Gol:
    """
    Clase que representa un gol marcado en un partido.

    Attributes:
        id (int): Identificador único del gol
        partido_id (int): ID del partido
        jugador_id (int): ID del jugador que marcó
        minuto (int): Minuto en que se marcó el gol
    """

    def __init__(self, id=None, partido_id=None, jugador_id=None, minuto=None):
        """
        Inicializa un objeto Gol.
        """
        self.id = id
        self.partido_id = partido_id
        self.jugador_id = jugador_id
        self.minuto = minuto

    def guardar(self):
        """
        Guarda el gol en la base de datos.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO goles (partido_id, jugador_id, minuto)
            VALUES (?, ?, ?)
        """
        )
        query.addBindValue(self.partido_id)
        query.addBindValue(self.jugador_id)
        query.addBindValue(self.minuto)

        if query.exec():
            self.id = query.lastInsertId()
            return True
        else:
            print(f"Error al registrar gol: {query.lastError().text()}")
            return False

    def eliminar(self):
        """
        Elimina el gol de la base de datos.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.id:
            return False

        query = QSqlQuery()
        query.prepare("DELETE FROM goles WHERE id = ?")
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar gol: {query.lastError().text()}")
            return False

    @staticmethod
    def obtener_por_partido(partido_id):
        """
        Obtiene todos los goles de un partido específico.

        Args:
            partido_id (int): ID del partido

        Returns:
            list: Lista de diccionarios con información de goles
        """
        goles = []
        query = QSqlQuery()
        query.prepare(
            """
            SELECT g.id, g.partido_id, g.jugador_id, g.minuto, COUNT(*) as cantidad
            FROM goles g
            WHERE g.partido_id = ?
            GROUP BY g.jugador_id
            ORDER BY g.minuto
        """
        )
        query.addBindValue(partido_id)

        if query.exec():
            while query.next():
                goles.append(
                    {
                        "id": query.value(0),
                        "partido_id": query.value(1),
                        "jugador_id": query.value(2),
                        "minuto": query.value(3),
                        "cantidad": query.value(4),
                    }
                )

        return goles

    @staticmethod
    def obtener_por_jugador(jugador_id):
        """
        Obtiene todos los goles de un jugador específico.

        Args:
            jugador_id (int): ID del jugador

        Returns:
            list: Lista de objetos Gol
        """
        goles = []
        query = QSqlQuery()
        query.prepare(
            "SELECT * FROM goles WHERE jugador_id = ? ORDER BY partido_id, minuto"
        )
        query.addBindValue(jugador_id)

        if query.exec():
            while query.next():
                goles.append(
                    Gol(
                        id=query.value(0),
                        partido_id=query.value(1),
                        jugador_id=query.value(2),
                        minuto=query.value(3),
                    )
                )

        return goles

    @staticmethod
    def contar_goles_jugador(jugador_id):
        """
        Cuenta cuántos goles ha marcado un jugador.

        Args:
            jugador_id (int): ID del jugador

        Returns:
            int: Número de goles
        """
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM goles WHERE jugador_id = ?")
        query.addBindValue(jugador_id)

        if query.exec() and query.next():
            return query.value(0)
        return 0

    @staticmethod
    def eliminar_por_partido(partido_id):
        """
        Elimina todos los goles de un partido.

        Args:
            partido_id (int): ID del partido

        Returns:
            bool: True si se eliminaron correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare("DELETE FROM goles WHERE partido_id = ?")
        query.addBindValue(partido_id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar goles del partido: {query.lastError().text()}")
            return False

    @staticmethod
    def registrar_goles_partido(partido_id, jugador_id, cantidad, minuto_inicial=None):
        """
        Registra múltiples goles de un jugador en un partido.

        Args:
            partido_id (int): ID del partido
            jugador_id (int): ID del jugador
            cantidad (int): Cantidad de goles a registrar
            minuto_inicial (int, optional): Minuto inicial (incrementará para cada gol)

        Returns:
            bool: True si se registraron todos los goles correctamente
        """
        exito = True
        for i in range(cantidad):
            minuto = minuto_inicial + i if minuto_inicial is not None else None
            gol = Gol(partido_id=partido_id, jugador_id=jugador_id, minuto=minuto)
            if not gol.guardar():
                exito = False

        return exito

    def __repr__(self):
        """
        Representación técnica del gol.

        Returns:
            str: Representación con atributos principales
        """
        return f"Gol(id={self.id}, partido_id={self.partido_id}, jugador_id={self.jugador_id}, minuto={self.minuto})"
