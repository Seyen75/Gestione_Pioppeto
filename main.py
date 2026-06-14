import os
import sys
# Aggiunta del percorso della cartella del progetto alla variabile d'ambiente PYTHONPATH per garantire che tutte le importazioni funzionino correttamente indipendentemente da dove viene eseguito lo script
from GUI.pioppeto_main import PioppetoMain
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

# Trova il percorso assoluto della cartella che contiene questo file main.py, che è la radice del progetto Gestione_Pioppeto
cartella_progetto = os.path.dirname(os.path.abspath(__file__))

# Sposta la cartella di lavoro corrente di Python dentro Gestione_Pioppeto
os.chdir(cartella_progetto)

# Inserisci questa cartella in cima alla lista dei percorsi di ricerca dei moduli
if cartella_progetto not in sys.path:
    sys.path.insert(0, cartella_progetto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Crea e applica una Dark Palette globale per un tema scuro coerente in tutta l'applicazione, 
    # con colori personalizzati per sfondi, testi, bottoni e selezioni, migliorando l'estetica e la leggibilità in ambienti a bassa luminosità
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(20, 25, 35))          # Sfondo principale finestre (#141923)
    palette.setColor(QPalette.WindowText, Qt.white)                # Testo principale
    palette.setColor(QPalette.Base, QColor(35, 40, 50))            # Sfondo di tabelle, menu a tendina (ComboBox) e campi testo
    palette.setColor(QPalette.AlternateBase, QColor(45, 50, 60))   # Colore righe alternate nelle tabelle
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.white)                      # Testo dentro le tabelle/combobox
    palette.setColor(QPalette.Button, QColor(45, 50, 60))          # Sfondo bottoni generici
    palette.setColor(QPalette.ButtonText, Qt.white)                # Testo bottoni
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(183, 28, 28))      # Colore selezione (es. un rosso scuro)
    palette.setColor(QPalette.HighlightedText, Qt.white)           # Testo dell'elemento selezionato
    
    app.setPalette(palette)
    
    # Forza via CSS le aberrazioni specifiche di Windows sui menu a tendina (QComboBox), 
    # garantendo che anche su piattaforme Windows i menu a tendina abbiano uno sfondo scuro coerente con il tema generale dell'applicazione, 
    # con testo bianco e evidenziazione rossa per gli elementi selezionati
    app.setStyleSheet("""
        QComboBox QAbstractItemView {
            background-color: #232832;
            color: white;
            selection-background-color: #b71c1c;
        }
    """)
    
    finestra = PioppetoMain()
    finestra.show()
    sys.exit(app.exec())