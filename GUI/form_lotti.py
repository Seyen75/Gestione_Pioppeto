# Modulo per il pannello di controllo e pianificazione del pioppeto.

import random

from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from GUI.utils import centra_finestra, mostra_messaggio_stilizzato
from Core.lotto import Lotto
from Core.servizi import ServizioSelvicolturale

class FormLotti(QWidget):
    def __init__(self, parametri_condivisi, dizionario_cloni, parent=None):
        super().__init__(parent)

        if parent:
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # Caricamento UI
        loader = QUiLoader()
        self.ui_interfaccia = loader.load("GUI/form_lotti.ui", None)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui_interfaccia)
        layout.setContentsMargins(10, 10, 10, 10)
        self.DIM_W = 647
        self.DIM_H = 721

        self.setWindowTitle("Gestione Lotti Colturali")
        self.parametri = parametri_condivisi
        self.dizionario_cloni = dizionario_cloni

        # AGGANCIO WIDGET
        self.txt_id_lotto = self.ui_interfaccia.findChild(object, "txt_id_lotto")
        self.spin_ettari = self.ui_interfaccia.findChild(object, "spin_ettari")
        self.combo_clone = self.ui_interfaccia.findChild(object, "combo_clone")
        self.combo_sesto_impianto = self.ui_interfaccia.findChild(object, "combo_sesto_impianto")
        self.spin_attrito = self.ui_interfaccia.findChild(object, "spin_attrito")
        self.spin_test_idrico = self.ui_interfaccia.findChild(object, "spin_test_idrico")
        self.table_lotti = self.ui_interfaccia.findChild(object, "table_lotti")
        self.combo_destinazione = self.ui_interfaccia.findChild(object, "combo_destinazione")
        self.lbl_avviso_clone = self.ui_interfaccia.findChild(object, "lbl_avviso_clone")
        self.spin_eta_iniziale = self.ui_interfaccia.findChild(object, "spin_eta_iniziale")

        # Configurazione Tabella
        self.table_lotti.setColumnCount(6)
        self.table_lotti.setSelectionBehavior(self.table_lotti.SelectionBehavior.SelectRows)
        self.table_lotti.setSelectionMode(self.table_lotti.SelectionMode.SingleSelection)
        self.table_lotti.verticalHeader().setVisible(False)

        # Pulsanti
        self.btn_azione = self.ui_interfaccia.findChild(object, "btn_azione_lotto")
        self.btn_secondario = self.ui_interfaccia.findChild(object, "btn_elimina_lotto")
        self.btn_randomizza = self.ui_interfaccia.findChild(object, "btn_randomizza")
        self.btn_esci = self.ui_interfaccia.findChild(object, "btn_esci")

        # Connessioni
        self.btn_azione.clicked.connect(self.gestisci_azione_pulsante_principale)
        self.btn_secondario.clicked.connect(self.gestisci_azione_pulsante_secondario)
        self.btn_randomizza.clicked.connect(self.genera_lotto_casuale)
        self.btn_esci.clicked.connect(self.close)
        
        self.table_lotti.itemSelectionChanged.connect(self.carica_lotto_selezionato)
        self.combo_clone.currentTextChanged.connect(self.verifica_coerenza_selvicolturale)
        self.combo_destinazione.currentTextChanged.connect(self.verifica_coerenza_selvicolturale)

        # Inizializzazione
        self.popola_combo_iniziali()
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    def showEvent(self, event):
        super().showEvent(event)
        centra_finestra(self, self.DIM_W, self.DIM_H)
          
    def popola_combo_iniziali(self):
        ''' Carica i dati all'interno dei controlli combobox presenti sulla form '''
        self.combo_clone.blockSignals(True)
        self.combo_destinazione.blockSignals(True)
        self.combo_sesto_impianto.blockSignals(True)
        
        self.combo_clone.addItems(list(self.dizionario_cloni.keys()))
        self.combo_sesto_impianto.addItems(["3x2", "3x3", "6x6", "6x5", "7x6", "7x7"])
        self.combo_destinazione.addItems(["OPERA", "INDUSTRIA"])
        
        self.combo_clone.blockSignals(False)
        self.combo_destinazione.blockSignals(False)
        self.combo_sesto_impianto.blockSignals(False)

    def aggiungi_nuovo_lotto(self):
        '''Aggiunge il nuovo lotto con i dati inseriti nei controlli della form dopo averne validato i valori '''
        if not self.valida_dati_input(): return

        # Istanzia il nuovo oggetto Lotto fornendo i dati base al costruttore e successivamente inserisce i valori presenti nella form
        nuovo_lotto = Lotto(id_lotto = self.txt_id_lotto.text(), superficie = self.spin_ettari.value())
        nuovo_lotto.sesto_impianto = self.combo_sesto_impianto.currentText()
        nuovo_lotto.destinazione_uso = self.combo_destinazione.currentText()
        nuovo_lotto.clone_assegnato = self.combo_clone.currentText()
        nuovo_lotto.eta = self.spin_eta_iniziale.value()
        nuovo_lotto.indice_attrito_spaziale = int(self.spin_attrito.value())
        nuovo_lotto.indice_tendenza_idrica = float(self.spin_test_idrico.value())

        # Calcola la densità di piante iniziali attraverso la tipologia del sesto d'impianto
        nuovo_lotto.densita_iniziale = ServizioSelvicolturale.calcola_densita_iniziale(nuovo_lotto.sesto_impianto)
        
        nuovo_lotto.inizializza_nuovo_ciclo()
        # Aggiunge il nuovo lotto alla collezione di lotti della simulazione
        self.parametri.collezione_lotti.append(nuovo_lotto)
        
        # Resetta i controlli dell'interfaccia per avviare un nuovo inserimento ed aggiorna la tabella con il nuovo lotto creato
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    def salva_modifica_lotto(self):
        '''Registra le modifiche effettuate al lotto selezionato dalla tabella'''
        
        # Verifica se la riga selezionata ha dati coerenti
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe or not self.valida_dati_input(): return

        # recupera dalla collezione dei lotti il lotto con codice della riga selezionata
        lotto = self.parametri.collezione_lotti[righe[0].row()]

        # delega la funzione della classe lotto l'aggiornamento dei parametri strutturali, come il numero di piante
        lotto.aggiorna_parametri_strutturali(self.spin_ettari.value(), self.combo_sesto_impianto.currentText())
        
        # aggiorna i dati del lotto con i nuovi valori inseriti nella form
        lotto.indice_attrito_spaziale = int(self.spin_attrito.value())
        lotto.indice_tendenza_idrica = float(self.spin_test_idrico.value())
        lotto.eta = self.spin_eta_iniziale.value()
        lotto.clone_assegnato = self.combo_clone.currentText()
        lotto.destinazione_uso = self.combo_destinazione.currentText()

        # se siamo al primo anno e nella stagione invernale allora inizializza il lotto come primo ciclo
        if self.parametri.anno_corrente == 1 and self.parametri.stagione_corrente == "Inverno":
            lotto.inizializza_nuovo_ciclo()

        # Resetta i controlli dell'interfaccia ed aggiorna la tabella con i valori modificati
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    def genera_lotto_casuale(self):
        '''Funzione per generale un lotto totalmente in maniera casuale.
           Creare un lotto random potrebbe portare a importanti inefficienze della simulazione e fallimento operativi'''
        
        # istanzia il nuovo lotto ed impone un valore random di estensione fra i valori 1 e 30. Tale valore massimo per evitare la creazione di lotti eccessivamente grandi  
        lotto_random = Lotto(self.calcola_prossimo_id_progressivo(), round(random.uniform(1, 30.0), 1))
       
        # selezione random fra i vari sesti di impianto presenti e l'età dei lotti differenziandoli per la destinazione d'uso
        lotto_random.clone_assegnato = random.choice(list(self.dizionario_cloni.keys()))
        lotto_random.destinazione_uso = random.choice(["OPERA", "INDUSTRIA"])
        if lotto_random.destinazione_uso == "OPERA":
            lotto_random.sesto_impianto = random.choice(["6x6", "6x5", "7x6", "7x7"])
            lotto_random.eta = random.randint(0, 10)
        else:
            lotto_random.sesto_impianto = random.choice(["3x3", "3x2"])
            lotto_random.eta = random.randint(0, 5)
        lotto_random.densita_iniziale = ServizioSelvicolturale.calcola_densita_iniziale(lotto_random.sesto_impianto)
        
        # Aggiunta dei restanti parametri del lotto tramite la funzione random e limiti
        lotto_random.indice_attrito_spaziale = random.randint(0, 10)
        lotto_random.indice_tendenza_idrica = round(random.uniform(-1.0, 1.0), 2)
        

        
        lotto_random.inizializza_nuovo_ciclo()
        self.parametri.collezione_lotti.append(lotto_random)
        self.aggiorna_tabella_da_modello()

    def elimina_lotto_selezionato(self):
        '''Elimina il lotto selezionato sulla riga tabella'''
        # verifica se ci sono righe nella tabella
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe: return

        risposta = mostra_messaggio_stilizzato(
            self, "Conferma Eliminazione", "Sei sicuro di voler eliminare permanentemente il lotto selezionato?", "domanda"
        )
        if risposta == QMessageBox.StandardButton.Yes:
            # eliminazione del lotto dalla collezione e resetta i controlli sulla form
            self.parametri.collezione_lotti.pop(righe[0].row())
            self.svuota_e_resetta_interfaccia()
            self.aggiorna_tabella_da_modello()

    def carica_lotto_selezionato(self):
        '''Carica i valori della riga selezionata sui controlli della form per consentire le modifiche'''
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe: return

        lotto = self.parametri.collezione_lotti[righe[0].row()]
        self.txt_id_lotto.setText(lotto.id_lotto)
        self.spin_ettari.setValue(lotto.superficie_ettari)
        self.spin_attrito.setValue(lotto.indice_attrito_spaziale)
        self.spin_test_idrico.setValue(lotto.indice_tendenza_idrica)
        self.spin_eta_iniziale.setValue(lotto.eta)
        
        # Imposta i valori dei vari combobox
        self.combo_clone.setCurrentIndex(self.combo_clone.findText(lotto.clone_assegnato))
        self.combo_sesto_impianto.setCurrentIndex(self.combo_sesto_impianto.findText(lotto.sesto_impianto))
        self.combo_destinazione.setCurrentIndex(self.combo_destinazione.findText(lotto.destinazione_uso))

        self.btn_azione.setText("Aggiorna")
        self.btn_secondario.setText("Elimina")

    def svuota_e_resetta_interfaccia(self):
        '''Azzera i valori dei controlli dell'interfaccia'''
        self.table_lotti.clearSelection()
        self.txt_id_lotto.setText(self.calcola_prossimo_id_progressivo())
        self.spin_ettari.setValue(0.0)
        self.spin_attrito.setValue(0)
        self.spin_test_idrico.setValue(0.0)
        self.spin_eta_iniziale.setValue(0)
        self.btn_azione.setText("Aggiungi Lotto")
        self.btn_secondario.setText("Svuota")
        self.verifica_coerenza_selvicolturale()

    def verifica_coerenza_selvicolturale(self):
        '''Ottiene dal servizio il testo da inserire nella label che avverte se il clone selezionato è idoneo alla destinazione d'uso scelto'''
        
        destinazione = self.combo_destinazione.currentText()
        clone = self.combo_clone.currentText()
        
        risultato = ServizioSelvicolturale.ottieni_messaggio_coerenza(
           clone, destinazione, 
            self.dizionario_cloni.get(self.combo_clone.currentText(), {})
        )
        self.lbl_avviso_clone.setText(risultato["testo"])
        self.lbl_avviso_clone.setStyleSheet(risultato["stile"])

    def aggiorna_tabella_da_modello(self):
        '''Imposta la struttura della tabella popolando le celle delle righe'''
        # Carica la collezione dei lotti in una variabile locale
        lotti = self.parametri.collezione_lotti
        self.table_lotti.setRowCount(len(lotti))
        # Cicla per ogni riga con ogni lotto
        for riga, lotto in enumerate(lotti):
            # Crea una lista dove inserire i dati necessari per l'inserimento dei valori nelle celle della riga
            dati = [str(lotto.id_lotto), f"{lotto.superficie_ettari:.2f} ha", str(lotto.clone_assegnato), 
                    str(lotto.sesto_impianto), f"{lotto.eta} anni", str(lotto.destinazione_uso)]
            for col, val in enumerate(dati):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Evita che le celle possano essere direttamente modificabili su tabella
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_lotti.setItem(riga, col, item)

    def valida_dati_input(self) -> bool:
        '''funzione per aggiungere gli eventuali paramentri di verifica sui dati inseriti'''
        
        if self.combo_destinazione.currentText() == "OPERA" and (self.combo_sesto_impianto.currentText()  == "3x2" or self.combo_sesto_impianto.currentText()   == "3x3"):
            mostra_messaggio_stilizzato(self, "Errore", "Per una destinazione OPERA non usare sesti di impianto 3x2 o 3x3", "critico")
            return False
        
        if self.combo_destinazione.currentText()  == "INDUSTRIA" and (self.combo_sesto_impianto.currentText()  == "6x6"
                                                               or self.combo_sesto_impianto.currentText()  == "6x5"
                                                               or self.combo_sesto_impianto.currentText()  == "7x6"
                                                               or self.combo_sesto_impianto.currentText()  == "7x7"):
            mostra_messaggio_stilizzato(self, "Errore", "Per una destinazione INDUSTRIA non usare sesti di impianto 6x6, 6x5, 7x6 o 7x7", "critico")
            return False
        
        # Lotti sopra i 100 ettari sono considerati eccessivi per la simulazione
        if self.spin_ettari.value() > 100.0:
            mostra_messaggio_stilizzato(self, "Errore", "Superficie fuori scala (>100 ha).", "critico")
            return False
        return True

    def calcola_prossimo_id_progressivo(self) -> str:
        '''Crea automaticamente il valore dell'id del lotto in maniera automatica e progressiva'''
        return f"LTI-{len(self.parametri.collezione_lotti) + 1:03d}"

    def gestisci_azione_pulsante_principale(self):
        '''Modifica il testo del tasto principale a seconda se si aggiunge o aggiorna un dato'''
        self.aggiungi_nuovo_lotto() if self.btn_azione.text() == "Aggiungi Lotto" else self.salva_modifica_lotto()

    def gestisci_azione_pulsante_secondario(self):
        '''modifica il testo del pulsante a seconda se si sta aggiornando un valore selezionato oppure si resettano i dati inseriti del nuovo lotto'''
        self.svuota_e_resetta_interfaccia() if self.btn_secondario.text() == "Svuota" else self.elimina_lotto_selezionato()