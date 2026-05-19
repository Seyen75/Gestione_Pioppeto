import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtUiTools import QUiLoader

class PioppetoMain(QMainWindow):
    def __init__(self):
        super().__init__()

        # Caricamento dinamico dell'interfaccia creata con il QT Designer
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "pioppeto_main.ui")
        self.ui_interfaccia = loader.load(percorso_ui, self)
        self.setCentralWidget(self.ui_interfaccia.centralWidget())

        # Titolo della form
        self.setWindowTitle("Gestione Avanzata per Sistemi di Pioppicoltura")

        # Collegamento dei widget QPushButton della form
        # Uso findChild che è il metodo nativo e sicuro per recuperare i widget da QUiLoader
        btn_esci = self.findChild(QPushButton, "btn_esci")
        btn_impostazioni = self.findChild(QPushButton, "btn_impostazioni")
        btn_ditta = self.findChild(QPushButton, "btn_gestione_ditta")
        btn_lotti = self.findChild(QPushButton, "btn_gestione_lotti")
        btn_simulazione = self.findChild(QPushButton, "btn_simulazione")
        btn_valutazioni = self.findChild(QPushButton, "btn_valutazioni")

        # Collegamento dei PushButton della form con i relativi metodi che gestiscono il click
        if btn_esci: btn_esci.clicked.connect(self.close)
        if btn_impostazioni: btn_impostazioni.clicked.connect(self.impostazioni)
        if btn_ditta: btn_ditta.clicked.connect(self.ditta)
        if btn_lotti: btn_lotti.clicked.connect(self.lotti)
        if btn_simulazione: btn_simulazione.clicked.connect(self.simulazione)
        if btn_valutazioni: btn_valutazioni.clicked.connect(self.valutazione)

        # Gestione dinamica dello sfondo per evitare il problema di compatibilità del path di ricerca delle risorse grafiche
        percorso_reale = os.path.join(os.path.dirname(__file__), "risorse", "sfondo_main.jpg")
        percorso_reale = percorso_reale.replace("\\", "/")

        if self.centralWidget():
            css_designer = self.centralWidget().styleSheet()
            # Sostituzione del percorso virtuale con quello reale del disco
            css_corretto = css_designer.replace(":/sfondo_main.jpg", percorso_reale)
            self.centralWidget().setStyleSheet(css_corretto)

        # Effetto Ombra Tridimensionale sul titolo
        self.label_titolo = self.findChild(QWidget, "label_titolo")

        if self.label_titolo:
            # Applicazione effetto ombra nativo di Qt
            ombra = QGraphicsDropShadowEffect(self)
            ombra.setBlurRadius(8)
            ombra.setXOffset(3)
            ombra.setYOffset(3)
            ombra.setColor(QColor(0, 0, 0, 200))

            # Applicazione effetto alla label del titolo
            self.label_titolo.setGraphicsEffect(ombra)

    # METODI GESTIONE AZIONI BOTTONI

    def impostazioni(self):
        print("Avvio finestra impostazioni")

    def ditta(self):
        print("Avvio finestra gestione ditta")

    def lotti(self):
        print("Avvio finestra gestione lotti")

    def simulazione(self):
        print("Avvio finestra simulazione")

    def valutazione(self):
        print("Avvio finestra valutazione")