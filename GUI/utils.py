
# Utility grafiche condivise per l'interfaccia utente del simulatore. Finestre di Messaggio personalizzate rispetto alle QMessageBox
# Sincronizzata per macOS per evitare lag e warning sui font.

from PySide6.QtWidgets import QMessageBox

def mostra_messaggio_stilizzato(parent, titolo, testo, tipo="info"):
    #Genera un QMessageBox personalizzato, compatto (400x160) e stilizzato
    # coerente con la Palette scura del simulatore.
    
    msg = QMessageBox(parent)
    msg.setWindowTitle(titolo)
    msg.setText(testo)
    
    # Configurazione del font di sistema nativo Mac (effettuato per garantire la compatibilità con i sistemi Mac)
    font_sistema = msg.font()
    font_sistema.setPointSize(13)
    msg.setFont(font_sistema)
    
    # Smistamento icone e pulsanti in base al tipo di messaggio
    if tipo == "critico":
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    elif tipo == "avviso":
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    elif tipo == "domanda":
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    else:
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

    # Impostazione fissa grandezza della finestra di messaggio per ottimizzarsi al resto
    msg.setFixedSize(400, 160)

    # Foglio di stile CSS scuro e compatto
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #1e2424; 
            border: 1px solid #34495e;
            border-radius: 8px;
        }
        QLabel {
            color: #eceff1;            
            padding-left: 10px;
            padding-right: 15px;
        }
        QPushButton {
            background-color: #2e7d32; 
            color: white;
            font-weight: bold;
            border-radius: 4px;
            padding: 6px 18px;
            margin-right: 5px;
            min-width: 65px;
        }
        QPushButton:hover {
            background-color: #388e3c; 
        }
        QPushButton:pressed {
            background-color: #1b5e20;
        }
    """)
    
    return msg.exec()