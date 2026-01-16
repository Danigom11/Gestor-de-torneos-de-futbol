import sys
import os
from PySide6.QtWidgets import QApplication

# Add workspace to path
sys.path.append(os.getcwd())

try:
    # We need a qApp instance for QSqlDatabase to work properly often
    app = QApplication(sys.argv)

    from Models import database
    from Models.partido import Partido

    # Init DB
    if not database.conectar():
        print("Failed to connect to DB")
        sys.exit(1)

    partidos = Partido.obtener_todos()
    print(f"Total partidos: {len(partidos)}")

    counts = {}
    for p in partidos:
        elim = p.eliminatoria
        counts[elim] = counts.get(elim, 0) + 1

    print("Conteo por ronda:")
    for k, v in counts.items():
        print(f"  {k}: {v}")

except Exception as e:
    import traceback

    traceback.print_exc()
