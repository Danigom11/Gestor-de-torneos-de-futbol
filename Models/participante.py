"""
Modelo de datos para la entidad Participante.

Este módulo contiene la clase Participante con todos los métodos CRUD
y operaciones relacionadas con jugadores y árbitros.
"""

from PySide6.QtSql import QSqlQuery
from datetime import datetime
import csv


class Participante:
    """
    Clase que representa un participante (jugador y/o árbitro) en el torneo.

    Attributes:
        id (int): Identificador único del participante
        nombre (str): Nombre completo del participante
        fecha_nacimiento (str): Fecha de nacimiento (formato YYYY-MM-DD)
        curso (str): Curso al que pertenece
        es_jugador (bool): Indica si es jugador
        es_arbitro (bool): Indica si es árbitro
        posicion (str): Posición en el campo (solo para jugadores)
        t_amarillas (int): Total de tarjetas amarillas
        t_rojas (int): Total de tarjetas rojas
        goles (int): Total de goles marcados
    """

    POSICIONES = ["Portero", "Defensa", "Centrocampista", "Delantero"]

    def __init__(
        self,
        id=None,
        nombre="",
        fecha_nacimiento="",
        curso="",
        es_jugador=False,
        es_arbitro=False,
        posicion="",
        t_amarillas=0,
        t_rojas=0,
        goles=0,
    ):
        """
        Inicializa un objeto Participante.

        Args:
            id (int, optional): ID del participante
            nombre (str): Nombre del participante
            fecha_nacimiento (str): Fecha de nacimiento
            curso (str): Curso del participante
            es_jugador (bool): Si es jugador
            es_arbitro (bool): Si es árbitro
            posicion (str): Posición en el campo
            t_amarillas (int): Tarjetas amarillas
            t_rojas (int): Tarjetas rojas
            goles (int): Goles marcados
        """
        self.id = id
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.curso = curso
        self.es_jugador = es_jugador
        self.es_arbitro = es_arbitro
        self.posicion = posicion if es_jugador else None
        self.t_amarillas = t_amarillas
        self.t_rojas = t_rojas
        self.goles = goles

    def calcular_edad(self):
        """
        Calcula la edad del participante.

        Returns:
            int: Edad en años, o None si no hay fecha de nacimiento
        """
        if not self.fecha_nacimiento:
            return None

        try:
            fecha_nac = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
            hoy = datetime.now()
            edad = hoy.year - fecha_nac.year
            if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1
            return edad
        except ValueError:
            return None

    def obtener_categoria(self):
        """
        Obtiene la categoría según la edad (normativa española).

        Returns:
            str: Categoría del jugador
        """
        edad = self.calcular_edad()
        if edad is None:
            return "Sin categoría"

        if edad < 12:
            return "Sub-12"
        elif edad < 14:
            return "Sub-14"
        elif edad < 16:
            return "Sub-16"
        elif edad < 18:
            return "Sub-18"
        else:
            return "Senior"

    def guardar(self):
        """
        Guarda el participante en la base de datos.
        Si el participante ya tiene ID, actualiza; si no, inserta nuevo.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if self.id:
            return self.actualizar()
        else:
            return self.crear()

    def crear(self):
        """
        Inserta un nuevo participante en la base de datos.

        Returns:
            bool: True si se insertó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO participantes 
            (nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion, t_amarillas, t_rojas, goles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        )
        query.addBindValue(self.nombre)
        query.addBindValue(self.fecha_nacimiento)
        query.addBindValue(self.curso)
        query.addBindValue(1 if self.es_jugador else 0)
        query.addBindValue(1 if self.es_arbitro else 0)
        query.addBindValue(self.posicion)
        query.addBindValue(self.t_amarillas)
        query.addBindValue(self.t_rojas)
        query.addBindValue(self.goles)

        if query.exec():
            self.id = query.lastInsertId()
            return True
        else:
            print(f"Error al crear participante: {query.lastError().text()}")
            return False

    def actualizar(self):
        """
        Actualiza los datos del participante en la base de datos.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        query.prepare(
            """
            UPDATE participantes 
            SET nombre = ?, fecha_nacimiento = ?, curso = ?, es_jugador = ?, 
                es_arbitro = ?, posicion = ?, t_amarillas = ?, t_rojas = ?, goles = ?
            WHERE id = ?
        """
        )
        query.addBindValue(self.nombre)
        query.addBindValue(self.fecha_nacimiento)
        query.addBindValue(self.curso)
        query.addBindValue(1 if self.es_jugador else 0)
        query.addBindValue(1 if self.es_arbitro else 0)
        query.addBindValue(self.posicion)
        query.addBindValue(self.t_amarillas)
        query.addBindValue(self.t_rojas)
        query.addBindValue(self.goles)
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al actualizar participante: {query.lastError().text()}")
            return False

    def eliminar(self):
        """
        Elimina el participante de la base de datos.

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if not self.id:
            return False

        query = QSqlQuery()
        query.prepare("DELETE FROM participantes WHERE id = ?")
        query.addBindValue(self.id)

        if query.exec():
            return True
        else:
            print(f"Error al eliminar participante: {query.lastError().text()}")
            return False

    @staticmethod
    def obtener_por_id(participante_id):
        """
        Obtiene un participante por su ID.

        Args:
            participante_id (int): ID del participante a buscar

        Returns:
            Participante: Objeto Participante si se encuentra, None en caso contrario
        """
        query = QSqlQuery()
        query.prepare("SELECT * FROM participantes WHERE id = ?")
        query.addBindValue(participante_id)

        if query.exec() and query.next():
            return Participante(
                id=query.value(0),
                nombre=query.value(1),
                fecha_nacimiento=query.value(2),
                curso=query.value(3),
                es_jugador=bool(query.value(4)),
                es_arbitro=bool(query.value(5)),
                posicion=query.value(6),
                t_amarillas=query.value(7),
                t_rojas=query.value(8),
                goles=query.value(9),
            )
        return None

    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los participantes de la base de datos.

        Returns:
            list: Lista de objetos Participante
        """
        participantes = []
        query = QSqlQuery("SELECT * FROM participantes ORDER BY nombre")

        while query.next():
            participantes.append(
                Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=bool(query.value(4)),
                    es_arbitro=bool(query.value(5)),
                    posicion=query.value(6),
                    t_amarillas=query.value(7),
                    t_rojas=query.value(8),
                    goles=query.value(9),
                )
            )

        return participantes

    @staticmethod
    def obtener_jugadores():
        """
        Obtiene todos los participantes que son jugadores.

        Returns:
            list: Lista de objetos Participante que son jugadores
        """
        participantes = []
        query = QSqlQuery(
            "SELECT * FROM participantes WHERE es_jugador = 1 ORDER BY nombre"
        )

        while query.next():
            participantes.append(
                Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=bool(query.value(4)),
                    es_arbitro=bool(query.value(5)),
                    posicion=query.value(6),
                    t_amarillas=query.value(7),
                    t_rojas=query.value(8),
                    goles=query.value(9),
                )
            )

        return participantes

    @staticmethod
    def obtener_arbitros():
        """
        Obtiene todos los participantes que son árbitros.

        Returns:
            list: Lista de objetos Participante que son árbitros
        """
        participantes = []
        query = QSqlQuery(
            "SELECT * FROM participantes WHERE es_arbitro = 1 ORDER BY nombre"
        )

        while query.next():
            participantes.append(
                Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=bool(query.value(4)),
                    es_arbitro=bool(query.value(5)),
                    posicion=query.value(6),
                    t_amarillas=query.value(7),
                    t_rojas=query.value(8),
                    goles=query.value(9),
                )
            )

        return participantes

    @staticmethod
    def obtener_jugadores_sin_equipo():
        """
        Obtiene los jugadores que no están asignados a ningún equipo.

        Returns:
            list: Lista de objetos Participante sin equipo
        """
        participantes = []
        query = QSqlQuery(
            """
            SELECT * FROM participantes 
            WHERE es_jugador = 1 
            AND id NOT IN (SELECT jugador_id FROM jugadores_equipos)
            ORDER BY nombre
        """
        )

        while query.next():
            participantes.append(
                Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=bool(query.value(4)),
                    es_arbitro=bool(query.value(5)),
                    posicion=query.value(6),
                    t_amarillas=query.value(7),
                    t_rojas=query.value(8),
                    goles=query.value(9),
                )
            )

        return participantes

    @staticmethod
    def buscar(texto):
        """
        Busca participantes por nombre o curso.

        Args:
            texto (str): Texto a buscar

        Returns:
            list: Lista de participantes que coinciden con la búsqueda
        """
        participantes = []
        query = QSqlQuery()
        query.prepare(
            """
            SELECT * FROM participantes 
            WHERE nombre LIKE ? OR curso LIKE ?
            ORDER BY nombre
        """
        )
        patron = f"%{texto}%"
        query.addBindValue(patron)
        query.addBindValue(patron)

        if query.exec():
            while query.next():
                participantes.append(
                    Participante(
                        id=query.value(0),
                        nombre=query.value(1),
                        fecha_nacimiento=query.value(2),
                        curso=query.value(3),
                        es_jugador=bool(query.value(4)),
                        es_arbitro=bool(query.value(5)),
                        posicion=query.value(6),
                        t_amarillas=query.value(7),
                        t_rojas=query.value(8),
                        goles=query.value(9),
                    )
                )

        return participantes

    @staticmethod
    def ordenar_por_goles(limite=None):
        """
        Obtiene los participantes ordenados por goles (descendente).

        Args:
            limite (int, optional): Número máximo de resultados

        Returns:
            list: Lista de participantes ordenados por goles
        """
        participantes = []
        sql = "SELECT * FROM participantes WHERE es_jugador = 1 ORDER BY goles DESC"
        if limite:
            sql += f" LIMIT {limite}"

        query = QSqlQuery(sql)

        while query.next():
            participantes.append(
                Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=bool(query.value(4)),
                    es_arbitro=bool(query.value(5)),
                    posicion=query.value(6),
                    t_amarillas=query.value(7),
                    t_rojas=query.value(8),
                    goles=query.value(9),
                )
            )

        return participantes

    @staticmethod
    def ordenar_por_tarjetas(tipo="total", limite=None):
        """
        Obtiene los participantes ordenados por tarjetas (descendente).

        Args:
            tipo (str): 'amarillas', 'rojas' o 'total'
            limite (int, optional): Número máximo de resultados

        Returns:
            list: Lista de participantes ordenados por tarjetas
        """
        participantes = []

        if tipo == "amarillas":
            orden = "t_amarillas DESC"
        elif tipo == "rojas":
            orden = "t_rojas DESC"
        else:
            orden = "(t_amarillas + t_rojas) DESC"

        sql = f"SELECT * FROM participantes WHERE es_jugador = 1 ORDER BY {orden}"
        if limite:
            sql += f" LIMIT {limite}"

        query = QSqlQuery(sql)

        while query.next():
            participantes.append(
                Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=bool(query.value(4)),
                    es_arbitro=bool(query.value(5)),
                    posicion=query.value(6),
                    t_amarillas=query.value(7),
                    t_rojas=query.value(8),
                    goles=query.value(9),
                )
            )

        return participantes

    @staticmethod
    def exportar_csv(ruta_archivo, filtro="todos"):
        """
        Exporta participantes a un archivo CSV.

        Args:
            ruta_archivo (str): Ruta donde guardar el archivo CSV
            filtro (str): 'todos', 'jugadores' o 'arbitros'

        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        try:
            if filtro == "jugadores":
                participantes = Participante.obtener_jugadores()
            elif filtro == "arbitros":
                participantes = Participante.obtener_arbitros()
            else:
                participantes = Participante.obtener_todos()

            with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    [
                        "ID",
                        "Nombre",
                        "Fecha Nacimiento",
                        "Edad",
                        "Categoría",
                        "Curso",
                        "Es Jugador",
                        "Es Árbitro",
                        "Posición",
                        "Goles",
                        "Tarjetas Amarillas",
                        "Tarjetas Rojas",
                    ]
                )

                for p in participantes:
                    escritor.writerow(
                        [
                            p.id,
                            p.nombre,
                            p.fecha_nacimiento,
                            p.calcular_edad(),
                            p.obtener_categoria(),
                            p.curso,
                            "Sí" if p.es_jugador else "No",
                            "Sí" if p.es_arbitro else "No",
                            p.posicion or "",
                            p.goles,
                            p.t_amarillas,
                            p.t_rojas,
                        ]
                    )

            return True
        except Exception as e:
            print(f"Error al exportar participantes a CSV: {e}")
            return False

    def __str__(self):
        """
        Representación en string del participante.

        Returns:
            str: Nombre del participante
        """
        return self.nombre

    def __repr__(self):
        """
        Representación técnica del participante.

        Returns:
            str: Representación con atributos principales
        """
        tipos = []
        if self.es_jugador:
            tipos.append("Jugador")
        if self.es_arbitro:
            tipos.append("Árbitro")
        tipo_str = "/".join(tipos) if tipos else "Sin tipo"
        return f"Participante(id={self.id}, nombre='{self.nombre}', tipo='{tipo_str}')"
