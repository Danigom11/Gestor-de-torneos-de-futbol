"""
Modelo de datos para la entidad Tarjeta.

Este módulo gestiona el registro de tarjetas (amarillas y rojas) en los partidos.
"""

from PySide6.QtSql import QSqlQuery


class Tarjeta:
    """
    Clase que representa una tarjeta (amarilla o roja) en un partido.

    Attributes:
        id (int): Identificador único de la tarjeta
        partido_id (int): ID del partido
        jugador_id (int): ID del jugador que recibió la tarjeta
        tipo (str): Tipo de tarjeta ('amarilla' o 'roja')
        minuto (int): Minuto en que se mostró la tarjeta
    """

    TIPO_AMARILLA = "amarilla"
    TIPO_ROJA = "roja"

    def __init__(
        self, id=None, partido_id=None, jugador_id=None, tipo="amarilla", minuto=None
    ):
        """
        Inicializa un objeto Tarjeta.
        """
        self.id = id
        self.partido_id = partido_id
        self.jugador_id = jugador_id
        self.tipo = tipo
        self.minuto = minuto

    def guardar(self):
        """
        Guarda la tarjeta en la base de datos.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO tarjetas (partido_id, jugador_id, tipo, minuto)
            VALUES (?, ?, ?, ?)
        """
        )
        query.addBindValue(self.partido_id)
        query.addBindValue(self.jugador_id)
        query.addBindValue(self.tipo)
        query.addBindValue(self.minuto)

        if query.exec():
            self.id = query.lastInsertId()
            return True
        else:
            print(f"Error al registrar tarjeta: {query.lastError().text()}")
            return False

    def eliminar(self):
        """
        Elimina la tarjeta de la base de datos.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.id:
            return False

        query = QSqlQuery()
        query.prepare("DELETE FROM tarjetas WHERE id = ?")
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar tarjeta: {query.lastError().text()}")
            return False

    @staticmethod
    def obtener_por_partido(partido_id):
        """
        Obtiene todas las tarjetas de un partido específico agrupadas por jugador.

        Args:
            partido_id (int): ID del partido

        Returns:
            list: Lista de diccionarios con información de tarjetas por jugador
        """
        tarjetas = []
        query = QSqlQuery()
        query.prepare(
            """
            SELECT 
                jugador_id,
                SUM(CASE WHEN tipo = 'amarilla' THEN 1 ELSE 0 END) as amarillas,
                SUM(CASE WHEN tipo = 'roja' THEN 1 ELSE 0 END) as rojas
            FROM tarjetas
            WHERE partido_id = ?
            GROUP BY jugador_id
        """
        )
        query.addBindValue(partido_id)

        if query.exec():
            while query.next():
                tarjetas.append(
                    {
                        "jugador_id": query.value(0),
                        "amarillas": query.value(1),
                        "rojas": query.value(2),
                    }
                )

        return tarjetas

    @staticmethod
    def obtener_por_jugador(jugador_id):
        """
        Obtiene todas las tarjetas de un jugador específico.

        Args:
            jugador_id (int): ID del jugador

        Returns:
            list: Lista de objetos Tarjeta
        """
        tarjetas = []
        query = QSqlQuery()
        query.prepare(
            "SELECT * FROM tarjetas WHERE jugador_id = ? ORDER BY partido_id, minuto"
        )
        query.addBindValue(jugador_id)

        if query.exec():
            while query.next():
                tarjetas.append(
                    Tarjeta(
                        id=query.value(0),
                        partido_id=query.value(1),
                        jugador_id=query.value(2),
                        tipo=query.value(3),
                        minuto=query.value(4),
                    )
                )

        return tarjetas

    @staticmethod
    def contar_tarjetas_jugador(jugador_id, tipo=None):
        """
        Cuenta cuántas tarjetas ha recibido un jugador.

        Args:
            jugador_id (int): ID del jugador
            tipo (str, optional): Tipo de tarjeta ('amarilla', 'roja', o None para todas)

        Returns:
            int: Número de tarjetas
        """
        query = QSqlQuery()

        if tipo:
            query.prepare(
                "SELECT COUNT(*) FROM tarjetas WHERE jugador_id = ? AND tipo = ?"
            )
            query.addBindValue(jugador_id)
            query.addBindValue(tipo)
        else:
            query.prepare("SELECT COUNT(*) FROM tarjetas WHERE jugador_id = ?")
            query.addBindValue(jugador_id)

        if query.exec() and query.next():
            return query.value(0)
        return 0

    @staticmethod
    def eliminar_por_partido(partido_id):
        """
        Elimina todas las tarjetas de un partido.

        Args:
            partido_id (int): ID del partido

        Returns:
            bool: True si se eliminaron correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare("DELETE FROM tarjetas WHERE partido_id = ?")
        query.addBindValue(partido_id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar tarjetas del partido: {query.lastError().text()}")
            return False

    @staticmethod
    def registrar_tarjetas_partido(
        partido_id, jugador_id, amarillas=0, rojas=0, minuto_inicial=None
    ):
        """
        Registra múltiples tarjetas de un jugador en un partido.

        Args:
            partido_id (int): ID del partido
            jugador_id (int): ID del jugador
            amarillas (int): Cantidad de tarjetas amarillas
            rojas (int): Cantidad de tarjetas rojas
            minuto_inicial (int, optional): Minuto inicial

        Returns:
            bool: True si se registraron todas las tarjetas correctamente
        """
        exito = True

        # Registrar tarjetas amarillas
        for i in range(amarillas):
            minuto = minuto_inicial + i if minuto_inicial is not None else None
            tarjeta = Tarjeta(
                partido_id=partido_id,
                jugador_id=jugador_id,
                tipo=Tarjeta.TIPO_AMARILLA,
                minuto=minuto,
            )
            if not tarjeta.guardar():
                exito = False

        # Registrar tarjetas rojas
        for i in range(rojas):
            minuto = (
                minuto_inicial + amarillas + i if minuto_inicial is not None else None
            )
            tarjeta = Tarjeta(
                partido_id=partido_id,
                jugador_id=jugador_id,
                tipo=Tarjeta.TIPO_ROJA,
                minuto=minuto,
            )
            if not tarjeta.guardar():
                exito = False

        return exito

    def __repr__(self):
        """
        Representación técnica de la tarjeta.

        Returns:
            str: Representación con atributos principales
        """
        return f"Tarjeta(id={self.id}, partido_id={self.partido_id}, jugador_id={self.jugador_id}, tipo='{self.tipo}', minuto={self.minuto})"
