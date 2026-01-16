"""Utilidades compartidas para las vistas.

- Resolución de rutas de recursos compatible con PyInstaller.
- Helpers de formato para QSS.
"""

from __future__ import annotations

import os
import sys


def obtener_ruta_recurso(ruta_relativa: str) -> str:
    """Obtiene la ruta absoluta de un recurso.

    Compatible con PyInstaller (sys._MEIPASS).
    """
    if getattr(sys, "frozen", False):
        ruta_base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        # Views/.. => raíz del proyecto
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(ruta_base, ruta_relativa)


def qss_url(path: str) -> str:
    """Convierte una ruta de Windows a formato usable por QSS (con '/')."""
    return path.replace("\\", "/")
