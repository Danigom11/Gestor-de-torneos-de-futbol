"""
Paquete de modelos para la aplicación de Gestión de Torneo de Fútbol.

Este paquete contiene todos los modelos de datos y la configuración de la base de datos.
"""

from . import database
from .equipo import Equipo
from .participante import Participante
from .partido import Partido
from .jugador_equipo import JugadorEquipo
from .gol import Gol
from .tarjeta import Tarjeta

__all__ = [
    "database",
    "Equipo",
    "Participante",
    "Partido",
    "JugadorEquipo",
    "Gol",
    "Tarjeta",
]
