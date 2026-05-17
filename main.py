import sys
from PySide6.QtWidgets import QApplication
from pioppeto_main import PioppetoMain

if __name__ == "__main__":

    # Inizializziazione l'applicazione Qt che comanda la parte grafica
    app = QApplication(sys.argv)

    # Istanza della finestra principale del simulatore e visualizzazione a schermo
    window = PioppetoMain()
    window.show()

    # Avvio ciclo degli eventi
    sys.exit(app.exec())