import os
import sys

# Trova il percorso assoluto della cartella che contiene QUESTO file main.py

cartella_progetto = os.path.dirname(os.path.abspath(__file__))

# Sposta la cartella di lavoro corrente di Python dentro Gestione_Pioppeto
os.chdir(cartella_progetto)

# Inserisci questa cartella in cima alla lista dei percorsi di ricerca dei moduli
if cartella_progetto not in sys.path:
    sys.path.insert(0, cartella_progetto)

from PySide6.QtWidgets import QApplication
from GUI.pioppeto_main import PioppetoMain

if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = PioppetoMain()
    finestra.show()
    sys.exit(app.exec())