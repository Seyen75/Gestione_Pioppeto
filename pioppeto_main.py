import os
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader

class PioppetoMain(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inizializa il metodo che si occupa di caricare la componente grafica della form
        loader = QUiLoader()

        # Percorso assoluto del file grafico
        percorso_ui = os.path.join(os.path.dirname(__file__), "pioppeto_main.ui")

        # Viene caricata la form nella classe PioppetoMain
        self.ui = loader.load(percorso_ui, self)

        # Aggancia l'interfaccia centrale della MainWindow creata nel Designer
        self.setCentralWidget(self.ui.centralWidget())

        self.setWindowTitle("Gestione avanzata di pioppicoltura")
