"""
Modelo de datos para la entidad Equipo.

Este módulo contiene la clase Equipo con todos los métodos CRUD
y operaciones relacionadas con la gestión de equipos.
"""

from PySide6.QtSql import QSqlQuery
from datetime import datetime
import csv
import os


class Equipo:
    """
    Clase que representa un equipo en el torneo.

    Attributes:
        id (int): Identificador único del equipo
        nombre (str): Nombre del equipo
        curso (str): Curso al que pertenece el equipo
        color (str): Color de la camiseta (código hexadecimal)
        escudo (str): Nombre del archivo del escudo
        fecha_creacion (str): Fecha de creación del equipo
    """

    def __init__(
        self, id=None, nombre="", curso="", color="", escudo="", fecha_creacion=""
    ):
        """
        Inicializa un objeto Equipo.

        Args:
            id (int, optional): ID del equipo
            nombre (str): Nombre del equipo
            curso (str): Curso del equipo
            color (str): Color de la camiseta
            escudo (str): Nombre del archivo del escudo
            fecha_creacion (str): Fecha de creación
        """
        self.id = id
        self.nombre = nombre
        self.curso = curso
        self.color = color
        self.escudo = escudo
        self.fecha_creacion = fecha_creacion or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def guardar(self):
        """
        Guarda el equipo en la base de datos.
        Si el equipo ya tiene ID, actualiza; si no, inserta nuevo.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if self.id:
            return self.actualizar()
        else:
            return self.crear()

    def crear(self):
        """
        Inserta un nuevo equipo en la base de datos.

        Returns:
            bool: True si se insertó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO equipos (nombre, curso, color, escudo, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        """
        )
        query.addBindValue(self.nombre)
        query.addBindValue(self.curso)
        query.addBindValue(self.color)
        query.addBindValue(self.escudo)
        query.addBindValue(self.fecha_creacion)

        if query.exec():
            self.id = query.lastInsertId()
            return True
        else:
            print(f"Error al crear equipo: {query.lastError().text()}")
            return False

    def actualizar(self):
        """
        Actualiza los datos del equipo en la base de datos.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            UPDATE equipos 
            SET nombre = ?, curso = ?, color = ?, escudo = ?
            WHERE id = ?
        """
        )
        query.addBindValue(self.nombre)
        query.addBindValue(self.curso)
        query.addBindValue(self.color)
        query.addBindValue(self.escudo)
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al actualizar equipo: {query.lastError().text()}")
            return False

    def eliminar(self):
        """
        Elimina el equipo de la base de datos.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.id:
            return False

        query = QSqlQuery()
        query.prepare("DELETE FROM equipos WHERE id = ?")
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar equipo: {query.lastError().text()}")
            return False

    @staticmethod
    def obtener_por_id(equipo_id):
        """
        Obtiene un equipo por su ID.

        Args:
            equipo_id (int): ID del equipo a buscar

        Returns:
            Equipo: Objeto Equipo si se encuentra, None en caso contrario
        """
        query = QSqlQuery()
        query.prepare("SELECT * FROM equipos WHERE id = ?")
        query.addBindValue(equipo_id)

        if query.exec() and query.next():
            return Equipo(
                id=query.value(0),
                nombre=query.value(1),
                curso=query.value(2),
                color=query.value(3),
                escudo=query.value(4),
                fecha_creacion=query.value(5),
            )
        return None

    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los equipos de la base de datos.

        Returns:
            list: Lista de objetos Equipo
        """
        equipos = []
        query = QSqlQuery("SELECT * FROM equipos ORDER BY nombre")

        while query.next():
            equipos.append(
                Equipo(
                    id=query.value(0),
                    nombre=query.value(1),
                    curso=query.value(2),
                    color=query.value(3),
                    escudo=query.value(4),
                    fecha_creacion=query.value(5),
                )
            )

        return equipos

    @staticmethod
    def buscar(texto):
        """
        Busca equipos por nombre o curso.

        Args:
            texto (str): Texto a buscar

        Returns:
            list: Lista de equipos que coinciden con la búsqueda
        """
        equipos = []
        query = QSqlQuery()
        query.prepare(
            """
            SELECT * FROM equipos 
            WHERE nombre LIKE ? OR curso LIKE ?
            ORDER BY nombre
        """
        )
        patron = f"%{texto}%"
        query.addBindValue(patron)
        query.addBindValue(patron)

        if query.exec():
            while query.next():
                equipos.append(
                    Equipo(
                        id=query.value(0),
                        nombre=query.value(1),
                        curso=query.value(2),
                        color=query.value(3),
                        escudo=query.value(4),
                        fecha_creacion=query.value(5),
                    )
                )

        return equipos

    @staticmethod
    def obtener_escudos_disponibles(ruta_escudos):
        """
        Obtiene la lista de escudos que no están siendo utilizados.

        Args:
            ruta_escudos (str): Ruta a la carpeta de escudos

        Returns:
            list: Lista de nombres de archivos de escudos disponibles
        """
        # Obtener todos los archivos SVG de la carpeta
        try:
            todos_escudos = [f for f in os.listdir(ruta_escudos) if f.endswith(".svg")]
        except FileNotFoundError:
            print(f"No se encontró la carpeta de escudos: {ruta_escudos}")
            return []

        # Obtener escudos en uso
        query = QSqlQuery("SELECT escudo FROM equipos")
        escudos_en_uso = []
        while query.next():
            escudos_en_uso.append(query.value(0))

        # Filtrar escudos disponibles
        escudos_disponibles = [e for e in todos_escudos if e not in escudos_en_uso]
        return sorted(escudos_disponibles)

    @staticmethod
    def contar_jugadores(equipo_id):
        """
        Cuenta cuántos jugadores tiene un equipo.

        Args:
            equipo_id (int): ID del equipo

        Returns:
            int: Número de jugadores del equipo
        """
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM jugadores_equipos WHERE equipo_id = ?")
        query.addBindValue(equipo_id)

        if query.exec() and query.next():
            return query.value(0)
        return 0

    @staticmethod
    def obtener_jugadores(equipo_id):
        """
        Obtiene todos los jugadores de un equipo.

        Args:
            equipo_id (int): ID del equipo

        Returns:
            list: Lista de diccionarios con información de los jugadores
        """
        jugadores = []
        query = QSqlQuery()
        query.prepare(
            """
            SELECT p.id, p.nombre, p.posicion, p.goles, p.t_amarillas, p.t_rojas
            FROM participantes p
            INNER JOIN jugadores_equipos je ON p.id = je.jugador_id
            WHERE je.equipo_id = ?
            ORDER BY p.nombre
        """
        )
        query.addBindValue(equipo_id)

        if query.exec():
            while query.next():
                jugadores.append(
                    {
                        "id": query.value(0),
                        "nombre": query.value(1),
                        "posicion": query.value(2),
                        "goles": query.value(3),
                        "t_amarillas": query.value(4),
                        "t_rojas": query.value(5),
                    }
                )

        return jugadores

    @staticmethod
    def tiene_partidos(equipo_id):
        """
        Verifica si un equipo tiene partidos programados o jugados.

        Args:
            equipo_id (int): ID del equipo

        Returns:
            bool: True si tiene partidos, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            SELECT COUNT(*) FROM partidos 
            WHERE equipo_local_id = ? OR equipo_visitante_id = ?
        """
        )
        query.addBindValue(equipo_id)
        query.addBindValue(equipo_id)

        if query.exec() and query.next():
            return query.value(0) > 0
        return False

    @staticmethod
    def exportar_csv(ruta_archivo):
        """
        Exporta todos los equipos a un archivo CSV.

        Args:
            ruta_archivo (str): Ruta donde guardar el archivo CSV

        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        try:
            equipos = Equipo.obtener_todos()

            with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    [
                        "ID",
                        "Nombre",
                        "Curso",
                        "Color",
                        "Escudo",
                        "Fecha Creación",
                        "Jugadores",
                    ]
                )

                for equipo in equipos:
                    num_jugadores = Equipo.contar_jugadores(equipo.id)
                    escritor.writerow(
                        [
                            equipo.id,
                            equipo.nombre,
                            equipo.curso,
                            equipo.color,
                            equipo.escudo,
                            equipo.fecha_creacion,
                            num_jugadores,
                        ]
                    )

            return True
        except Exception as e:
            print(f"Error al exportar equipos a CSV: {e}")
            return False

    def __str__(self):
        """
        Representación en string del equipo.

        Returns:
            str: Nombre del equipo
        """
        return self.nombre

    def __repr__(self):
        """
        Representación técnica del equipo.

        Returns:
            str: Representación con todos los atributos
        """
        return f"Equipo(id={self.id}, nombre='{self.nombre}', curso='{self.curso}')"
