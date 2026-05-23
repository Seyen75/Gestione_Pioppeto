
# Modulo Finestra principale (Dashboard) del simulatore di pioppicoltura.
# Gestisce i flussi di lavoro, il caricamento dinamico della UI e gli stati della barra delle applicazioni.

import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QGraphicsDropShadowEffect, QMessageBox, QApplication
from PySide6.QtGui import QColor
from PySide6.QtUiTools import QUiLoader

# Importazione delle risorse del Core
from Core.gestori_clone import GestoreCloni
from Core.ditta import Ditta
from Core.parametri_simulazione import ParametriSimulazione

# Importazione delle sotto-form grafiche
from GUI.form_ditta import FormDitta
from GUI.form_lotti import FormLotti

# Importazione del file system virtuale delle risorse per lo sfondo e le icone
import risorse.rc_risorse

class PioppetoMain(QMainWindow):
    def __init__(self):
        super().__init__()

        # CARICAMENTO DINAMICO INTERFACCIA
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "pioppeto_main.ui")
        ui_temporanea = loader.load(percorso_ui, None) 

        # Estrae in sicurezza il widget centrale prima che la UI temporanea svanisca
        widget_centrale = ui_temporanea.centralWidget()
        self.setCentralWidget(widget_centrale)

        self.setWindowTitle("Gestione Avanzata per Sistemi di Pioppicoltura")

        # INIZIALIZZAZIONE COMPONENTI NECESSARI PER LA SIMULAZIONE
        self.gestore_cloni = GestoreCloni()
        self.dizionario_cloni = self.gestore_cloni.carica_cloni() # Carica i 4 cloni scientifici

        # Crea l'unica istanza dell'oggetto Ditta e ParametriSimulazione che saranno utilizzate dalle varie form e dalla simulazione
        self.ditta_attiva = Ditta()
        self.parametri_condivisi = ParametriSimulazione()

        # Flag per tracciare se la simulazione è già stata calcolata
        self.simulazione_eseguita: bool = False

        # RECUPERO WIDGETS E COLLEGAMENTO AZIONI

        btn_esci = widget_centrale.findChild(QPushButton, "btn_esci")
        self.btn_ditta = widget_centrale.findChild(QPushButton, "btn_gestione_ditta")
        self.btn_lotti = widget_centrale.findChild(QPushButton, "btn_gestione_lotti")
        self.btn_simulazione = widget_centrale.findChild(QPushButton, "btn_simulazione")
        self.btn_monitoraggio = widget_centrale.findChild(QPushButton, "btn_monitoraggio")
        self.btn_valutazioni = widget_centrale.findChild(QPushButton, "btn_valutazioni")

        # Collegamento dei PushButton con i relativi metodi
        if btn_esci: btn_esci.clicked.connect(QApplication.instance().quit)
        if self.btn_ditta: self.btn_ditta.clicked.connect(self.ditta)
        if self.btn_lotti: self.btn_lotti.clicked.connect(self.lotti)
        if self.btn_simulazione: self.btn_simulazione.clicked.connect(self.simulazione)
        if self.btn_monitoraggio: self.btn_monitoraggio.clicked.connect(self.monitoraggio)
        if self.btn_valutazioni: self.btn_valutazioni.clicked.connect(self.valutazione)

        # GRAFICA DELLA FORM 
        
        # Sfondo della form inserito nello StyleSheet usato da QT per la grafica della form.
        self.setStyleSheet("""
            QMainWindow {
                border-image: url(:/sfondo_main.jpg) 0 0 0 0 stretch stretch;
            }
        """)

        # Effetto Ombra Tridimensionale sul titolo
        self.label_titolo = widget_centrale.findChild(QWidget, "label_titolo")
        if self.label_titolo:
            ombra = QGraphicsDropShadowEffect(self)
            ombra.setBlurRadius(8)
            ombra.setXOffset(3)
            ombra.setYOffset(3)
            ombra.setColor(QColor(0, 0, 0, 200))
            self.label_titolo.setGraphicsEffect(ombra)


        # VERIFICA STATO INIZIALE APPLICAZIONE

        self.aggiorna_stato_interfaccia()

    def aggiorna_stato_interfaccia(self):
        # Controlla i requisiti minimi delle classi per abilitare o disabilitare
        # i pulsanti sequenziali e aggiornare la barra di stato (StatusBar).
        
        # Requisito Ditta: Almeno un operaio inserito in inventario (Grado A o Grado B)
        ditta_pronta = (self.ditta_attiva.operai_grado_A + self.ditta_attiva.operai_grado_B) > 0

        # Requisito Lotti: Almeno un lotto presente nella collezione
        lotti_pronti = len(self.parametri_condivisi.collezione_lotti) > 0

        # CASO 1: Mancano i dati di base di ditta e/o lotti
        if not ditta_pronta or not lotti_pronti:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(False)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)

            if not ditta_pronta and not lotti_pronti:
                self.statusBar().showMessage("⚠️ Configurazione richiesta: inserire i dati della ditta e creare almeno un lotto.")
            elif not ditta_pronta:
                self.statusBar().showMessage("⚠️ Configurazione incompleta: configurare il personale ditta forestale.")
            else:
                self.statusBar().showMessage("⚠️ Configurazione incompleta: creare almeno un lotto colturale nel pioppeto.")

        # CASO 2: Dati sufficienti inseriti, pronti al lancio
        elif ditta_pronta and lotti_pronti and not self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(True)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)
            self.statusBar().showMessage("✅ Sistema pronto per la simulazione. Cliccare su 'Avvia Simulazione' per procedere.")

        # CASO 3: Simulazione completata con successo, sblocco output
        elif self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(True) # Permette una ri-esecuzione
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(True)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(True)
            self.statusBar().showMessage("📊 Simulazione completata con successo! Report e monitoraggi storici disponibili.")


    # METODI GESTIONE FINESTRE E FLUSSI

    def ditta(self):
        print("Avvio finestra gestione ditta")
        self.finestra_ditta = FormDitta(self.ditta_attiva, self)

        # Finestra avviata come modale per evitare che la form padre possa essere utilizzata erroneamente mentre si inseriscono i dati
        from PySide6.QtCore import Qt
        self.finestra_ditta.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.finestra_ditta.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_ditta.show()

    def lotti(self):
        print("Avvio finestra gestione lotti")
        self.finestra_lotti = FormLotti(self.parametri_condivisi, self)

        # Finestra avviata come modale per evitare che la form padre possa essere utilizzata erroneamente mentre si inseriscono i dati        
        from PySide6.QtCore import Qt
        self.finestra_lotti.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.finestra_lotti.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_lotti.show()

    def simulazione(self):
        print("Esecuzione ciclo lineare stocastico...")
        self.statusBar().showMessage("Inizializzazione del calcolo forestale in corso...")

        # Reset preventivo della simulazione per ripulire vecchi storici
        self.parametri_condivisi.reset_simulazione_globale()

        try:
            # SIMULAZIONE ANCORA DA CREARE --- QUI CI SARA' l'AVVIO ALLA FINESTRA DI SIMULAZIONE
            self.simulazione_eseguita = True
            QMessageBox.information(self, "Simulatore Forestale",
                                    "Simulazione completata.\nTutti i lotti aziendali hanno terminato il ciclo colturale e sono stati abbattuti.")
        except Exception as e:
            QMessageBox.critical(self, "Errore di Calcolo", f"Crash nel motore di simulazione:\n{str(e)}")
            self.simulazione_eseguita = False

        self.aggiorna_stato_interfaccia()

    def monitoraggio(self):
        # ANCORA DA IMPLEMENTARE
        print("Avvio finestra monitoraggio")
        self.statusBar().showMessage("Caricamento grafici di accrescimento e saturazione risorse...")

    def valutazione(self):
        # ANCORA DA IMPLEMENTARE
        print("Avvio finestra valutazione")
        self.statusBar().showMessage("Generazione report consuntivo finale ed efficienza capitale...")