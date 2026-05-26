# Modulo per il pannello di controllo e pianificazione del pioppeto.
# Gestisce l'inserimento dei lotti dall'Anno 0 e valida la coerenza selvicolturale dei cloni.

import os
import json
import random
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from GUI.utils import mostra_messaggio_stilizzato

from Core.lotto import Lotto

class FormLotti(QWidget):
    def __init__(self, parametri_condivisi, parent=None):
        super().__init__(parent)

        if parent:
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # Caricamento dinamico dell'interfaccia con QUiLoader
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_lotti.ui")
        self.ui_interfaccia = loader.load(percorso_ui, None)

        layout = QVBoxLayout(self)
        layout.addWidget(self.ui_interfaccia)
        layout.setContentsMargins(10, 10, 10, 10)

        self.setWindowTitle("Gestione Lotti Colturali")
        self.parametri = parametri_condivisi

        # AGGANCIO WIDGET DA INTERFACCIA
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

        # IMPOSTAZIONE TABELLA CON LISTA LOTTI INSERITI
        if self.table_lotti:
            self.table_lotti.setShowGrid(True)
            self.table_lotti.setColumnCount(6)
            
            orizzontale_header = self.table_lotti.horizontalHeader()
            orizzontale_header.setSectionResizeMode(orizzontale_header.ResizeMode.Interactive)
            
            # Impostiamo il comportamento specifico colonna per colonna per evitare la sovrapposizione degli header
            orizzontale_header.setSectionResizeMode(0, orizzontale_header.ResizeMode.ResizeToContents)
            orizzontale_header.setSectionResizeMode(1, orizzontale_header.ResizeMode.ResizeToContents)
            orizzontale_header.setSectionResizeMode(2, orizzontale_header.ResizeMode.Stretch)
            orizzontale_header.setSectionResizeMode(3, orizzontale_header.ResizeMode.ResizeToContents)
            orizzontale_header.setSectionResizeMode(4, orizzontale_header.ResizeMode.ResizeToContents)
            orizzontale_header.setSectionResizeMode(5, orizzontale_header.ResizeMode.Stretch)

            verticale_header = self.table_lotti.verticalHeader()
            verticale_header.setDefaultSectionSize(32)
            verticale_header.setVisible(False)
            self.table_lotti.setAlternatingRowColors(True)

        # AGGANCIO BOTTONI DA INTERFACCIA
        self.btn_azione = self.ui_interfaccia.findChild(object, "btn_azione_lotto")
        self.btn_secondario = self.ui_interfaccia.findChild(object, "btn_elimina_lotto")
        self.btn_randomizza = self.ui_interfaccia.findChild(object, "btn_randomizza")
        self.btn_esci = self.ui_interfaccia.findChild(object, "btn_esci")

        # L'ID Lotto non deve essere modificato ed è impostato in automatico dal sistema
        if self.txt_id_lotto:
            self.txt_id_lotto.setReadOnly(True)

        # IMPOSTAZIONI AZIONI BOTTONI
        if self.btn_azione:
            self.btn_azione.clicked.connect(self.gestisci_azione_pulsante_principale)
        if self.btn_secondario:
            self.btn_secondario.clicked.connect(self.gestisci_azione_pulsante_secondario)
        if self.btn_randomizza:
            self.btn_randomizza.clicked.connect(self.genera_lotto_casuale)
        if self.btn_esci:
            self.btn_esci.clicked.connect(self.esci)
        
        
        # IMPOSTAZIONI AZIONI TABELLA
        if self.table_lotti:
            self.table_lotti.itemSelectionChanged.connect(self.carica_lotto_selezionato)
            self.table_lotti.setSelectionBehavior(self.table_lotti.SelectionBehavior.SelectRows)
            self.table_lotti.setSelectionMode(self.table_lotti.SelectionMode.SingleSelection)

        # Verifica congruità della scelta del clone rispetto alla resa cercata, con segnalazione problema sulla label di riferimento
        if self.combo_clone:
            self.combo_clone.currentTextChanged.connect(self.verifica_coerenza_selvicolturale)
        if self.combo_destinazione:
            self.combo_destinazione.currentTextChanged.connect(self.verifica_coerenza_selvicolturale)

        # INIZIALIZZAZIONE DATI FORM
        self.popola_cloni_disponibili()
        self.popola_sesti_disponibili()
        self.popola_destinazioni_disponibili()

        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()


    def showEvent(self, event):
        # Funzione per inserimento grafico su schhermo della form coerentemente con la form padre
        super().showEvent(event)
        parent = self.parentWidget()
        if parent:
            geometria_parent = parent.geometry()
            larghezza_self = 647
            altezza_self = 664
            x = geometria_parent.x() + (geometria_parent.width() - larghezza_self) // 2
            y = geometria_parent.y() + (geometria_parent.height() - altezza_self) // 2
            self.move(x, y)

    def closeEvent(self, event):
        """Intercetta la chiusura della form per forzare l'aggiornamento dello stato della dashboard principale."""
        parent = self.parentWidget()
        if parent and hasattr(parent, "aggiorna_stato_interfaccia"):
            parent.aggiorna_stato_interfaccia()
        super().closeEvent(event)

    def popola_cloni_disponibili(self):
        # Carica la combobox con la lista dei cloni selezionabili
        if not self.combo_clone: return
        self.combo_clone.clear()

        percorso_base = os.path.dirname(os.path.dirname(__file__))
        percorso_json = os.path.join(percorso_base, "Core", "cloni.json")
        self.dizionario_cloni = {}

        try:
            if os.path.exists(percorso_json):
                with open(percorso_json, "r", encoding="utf-8") as f:
                    self.dizionario_cloni = json.load(f)
                if self.dizionario_cloni:
                    self.combo_clone.addItems(list(self.dizionario_cloni.keys()))
                    return
            raise FileNotFoundError
        except Exception:
            # Fallback se il file JSON è momentaneamente scollegato
            self.dizionario_cloni = {
                "I-214": {"attitudini": "OPERA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.85}},
                "I-45/51": {"attitudini": "INDUSTRIA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.90}},
                "Neva": {"attitudini": "OPERA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.88}},
                "Velasco": {"attitudini": "INDUSTRIA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.92}}
            }
            self.combo_clone.addItems(list(self.dizionario_cloni.keys()))

    def popola_sesti_disponibili(self):
        # Carica combobox delle tipologie di sesti di impianto utilizzabili
        if not self.combo_sesto_impianto: return
        self.combo_sesto_impianto.clear()
        self.combo_sesto_impianto.addItems(["6x6", "6x5", "7x6", "7x7"])

    def popola_destinazioni_disponibili(self):
        # Carica combobox con le tipologia di resa prevista per il lotto - OPERA (Legname da assi) o INDUSTRIA (Legname per cartiere)
        # Non è previsto la resa TRUCIOLATO in quanto è considerata resa secondaria dai lotti degradati o dagli scarti.
        if not self.combo_destinazione: return
        self.combo_destinazione.clear()
        self.combo_destinazione.addItems(["OPERA", "INDUSTRIA"])

    def Blacklist(self):
        # Mantenimento per consistenza con eventuali chiamate esterne ereditate
        pass

    def verifica_coerenza_selvicolturale(self):
        # Verifica si l'accoppiamento tra il Clone selezionato e la Destinazione d'uso commerciale è ottimale o crea un malus segnalandolo su apposita label.
        
        if not self.combo_clone or not self.combo_destinazione or not self.lbl_avviso_clone:
            return

        clone_scelto = self.combo_clone.currentText()
        destinazione_scelta = self.combo_destinazione.currentText().upper().strip()

        # mappatura di performances dei cloni con l'eventuale destinazione commerciale. Mappatura hard coded 
        mappatura_attitudini_cloni = {
                    "I-214": "OPERA",
                    "Neva": "OPERA",
                    "I-45/51": "INDUSTRIA",
                    "Velasco": "INDUSTRIA"
                }
       
        # Controllo se il clone selezionato è presente nel dizionario ed associa nel caso la sua destinazione commerciale. In caso non viene rilevato, affinchè non ci 
        # sia un crash dell'applicativo viene imposto il valore OPERA
        attitudine_reale = mappatura_attitudini_cloni.get(clone_scelto, "OPERA")

        if attitudine_reale == destinazione_scelta:
            self.lbl_avviso_clone.setText(f"✅ Abbinamento Ottimale: Il clone {clone_scelto} esprime il massimo potenziale per la filiera {destinazione_scelta}.")
            self.lbl_avviso_clone.setStyleSheet("color: #4CAF50; font-weight: bold; font-style: italic;")
        else:
            if destinazione_scelta == "OPERA":
                self.lbl_avviso_clone.setText(f"⚠️ Rischio Colturale: Il clone {clone_scelto} è selezionato per biomassa/cartiera. Produrrà nodi diffusi inficiando la resa in sfoglia.")
            else:
                self.lbl_avviso_clone.setText(f"⚠️ Eccesso Qualitativo: Il clone {clone_scelto} è genetizzato per compensati di pregio. Destinarlo a triturazione abbatte i margini di ditta.")
            self.lbl_avviso_clone.setStyleSheet("color: #FF9800; font-weight: bold; font-style: italic;")

    def calcola_prossimo_id_progressivo(self) -> str:
        # Calcola il primo valore libero per la numerazione consequenziale del lotto, al fine di evitare la presenza di lotti con ID uguale
        return f"LTI-{len(self.parametri.collezione_lotti) + 1:03d}"

    def aggiorna_tabella_da_modello(self):
        # Prende la collezione dei lotti eventualmente presente nell'applicativo e popola la tabella con i dati reali
        if not self.table_lotti: return
        self.table_lotti.setRowCount(0)

        for lotto in self.parametri.collezione_lotti:
            riga = self.table_lotti.rowCount()
            self.table_lotti.insertRow(riga)

            # Colonna 0: ID Lotto
            item_id = QTableWidgetItem(str(lotto.id_lotto))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_lotti.setItem(riga, 0, item_id)

            # Colonna 1: Superficie (ha)
            item_superficie = QTableWidgetItem(f"{lotto.superficie_ettari:.2f} ha")
            item_superficie.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_lotti.setItem(riga, 1, item_superficie)

            # Colonna 2: Clone Assegnato
            item_clone = QTableWidgetItem(str(lotto.clone_assegnato))
            item_clone.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_lotti.setItem(riga, 2, item_clone)

            # Colonna 3: Sesto d'Impianto
            item_sesto = QTableWidgetItem(str(lotto.sesto_impianto))
            item_sesto.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_lotti.setItem(riga, 3, item_sesto)

            # Colonna 4: Età Lotto (NUOVA COLONNA INTERCETTATA)
            eta_valore = lotto.eta if hasattr(lotto, 'eta') else 0
            item_eta = QTableWidgetItem(f"{eta_valore} anni")
            item_eta.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_lotti.setItem(riga, 4, item_eta)

            # Colonna 5: Destinazione d'Uso (OPERA / INDUSTRIA)
            item_dest = QTableWidgetItem(str(lotto.destinazione_uso))
            item_dest.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_lotti.setItem(riga, 5, item_dest)

    def valida_dati_input(self) -> bool:
        # Funzione per validazione della consistenza dei dati base
        ettari = self.spin_ettari.value()
        # Sono usate come finestra dei messaggi non la QMessageBox standard del modulo QT ma quella creata ad hoc
        if ettari <= 0.0:
            mostra_messaggio_stilizzato(self, "Errore Validazione", "La superficie deve essere maggiore di 0 ettari.", "avviso")
            return False
        if ettari > 100.0:
            mostra_messaggio_stilizzato(self, "Errore Critico", "Superficie fuori scala per singolo lotto (>100 ha).", "critico")
            return False
        return True

    def gestisci_azione_pulsante_principale(self):
        # Azione a seguito della pressione del tasto principale. Essendo un tasto dinamico, se è un nuovo lotto avvierà l'inserimento del nuovo lotto in tabella
        # Se è una modifica di un lotto caricato dalla tabella avvia la funzione di aggiornamento
        if self.btn_azione.text() == "Aggiungi Lotto":
            self.aggiungi_nuovo_lotto()
        else:
            self.salva_modifica_lotto()

    def gestisci_azione_pulsante_secondario(self):
        # Azione a seguito della pressione del tasto secondario. Essendo un tasto dinamico se non ci si trova con i dati caricati dalla tabella semplicemente inizializza i 
        # dati dei controlli a quelli standard. Altrimenti il bottone esegue l'eliminazione del lotto selezionato dalla lista e dalla tabella
        if self.btn_secondario.text() == "Svuota":
            self.svuota_e_resetta_interfaccia()
        else:
            self.elimina_lotto_selezionato()

    def aggiungi_nuovo_lotto(self):
        # Funzione per inserimento di un nuovo lotto nella lista dei lotti
        if not self.valida_dati_input(): return

        id_confermato = self.txt_id_lotto.text()
        # Si istanzia un nuovo oggetto della classe Lotto con inviati i dati necessari al costruttore di base
        nuovo_lotto = Lotto(id_lotto=id_confermato, superficie=self.spin_ettari.value())

        # Si inseriscono tutti i valori nelle variabili dell'oggetto Lotto presenti nei controlli
        nuovo_lotto.sesto_impianto = self.combo_sesto_impianto.currentText()
        lati = [float(x) for x in nuovo_lotto.sesto_impianto.split("x")]
        
        # La densità iniziale iniziale del lotto (numero di piantine posizionate appena nate).
        # Il calcolo moltiplica il numero di piantine per ettaro per il tipo di impianto scelto e poi lo moltiplica per l'estensione del lotto
        nuovo_lotto.densita_iniziale = int((10000 / (lati[0] * lati[1])) * self.spin_ettari.value())

        nuovo_lotto.indice_attrito_spaziale = int(self.spin_attrito.value()) if self.spin_attrito else 0
        nuovo_lotto.indice_tendenza_idrica = float(self.spin_test_idrico.value()) if self.spin_test_idrico else 0.0
        
        # Prepara il nuovo lotto impostando la biometria nominale di partenza
        if self.spin_eta_iniziale:
            nuovo_lotto.eta = self.spin_eta_iniziale.value()
            
        nuovo_lotto.clone_assegnato = self.combo_clone.currentText()
        nuovo_lotto.destinazione_uso = self.combo_destinazione.currentText()

        # Calcolo del moltiplicatore di efficienza (Malus se l'abbinamento è errato)
        dati_clone = self.dizionario_cloni.get(nuovo_lotto.clone_assegnato, {})
        attitudine = dati_clone.get("attitudini", "OPERA")
        if attitudine != "DUAL" and attitudine != nuovo_lotto.destinazione_uso:
            nuovo_lotto.moltiplicatore_efficienza_clone = 0.85
        else:
            nuovo_lotto.moltiplicatore_efficienza_clone = 1.0

        # Forza l'allineamento biometrico iniziale in base alla classe d'età immessa
        nuovo_lotto.inizializza_nuovo_ciclo()

        # Aggiunge il lotto alla collezione
        self.parametri.collezione_lotti.append(nuovo_lotto)
        
        # Azzera la form per un nuovo inserimento
        self.svuota_e_resetta_interfaccia()
        
        # Aggiorna la tabella dei lotti con il nuovo inserimento
        self.aggiorna_tabella_da_modello()

    def carica_lotto_selezionato(self):
        # Quando viene selezionata una riga sulla tabella vengono riportati i dati sui controlli per effettuare eventuali aggiornamenti o cancellazione
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe: return

        riga = righe[0].row()
        lotto = self.parametri.collezione_lotti[riga]

        self.txt_id_lotto.setText(lotto.id_lotto)
        self.spin_ettari.setValue(lotto.superficie_ettari)

        if self.spin_attrito: self.spin_attrito.setValue(lotto.indice_attrito_spaziale)
        if self.spin_test_idrico: self.spin_test_idrico.setValue(lotto.indice_tendenza_idrica)
        if self.spin_eta_iniziale and hasattr(lotto, 'eta'): self.spin_eta_iniziale.setValue(lotto.eta)

        index_clone = self.combo_clone.findText(lotto.clone_assegnato)
        if index_clone >= 0: self.combo_clone.setCurrentIndex(index_clone)

        index_sesto = self.combo_sesto_impianto.findText(lotto.sesto_impianto)
        if index_sesto >= 0: self.combo_sesto_impianto.setCurrentIndex(index_sesto)

        index_dest = self.combo_destinazione.findText(lotto.destinazione_uso)
        if index_dest >= 0: self.combo_destinazione.setCurrentIndex(index_dest)

        self.btn_azione.setText("Aggiorna")
        self.btn_secondario.setText("Elimina")

    def salva_modifica_lotto(self):
        # Salve le modifiche apportate ad un lotto già prensente in tabella e selezionato nei controlli
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe or not self.valida_dati_input(): return

        riga = righe[0].row()
        lotto = self.parametri.collezione_lotti[riga]

        lotto.superficie_ettari = self.spin_ettari.value()
        lotto.sesto_impianto = self.combo_sesto_impianto.currentText()
        lati = [float(x) for x in lotto.sesto_impianto.split("x")]
        lotto.densita_iniziale = int((10000 / (lati[0] * lati[1])) * self.spin_ettari.value())

        lotto.indice_attrito_spaziale = int(self.spin_attrito.value()) if self.spin_attrito else 0
        lotto.indice_tendenza_idrica = float(self.spin_test_idrico.value()) if self.spin_test_idrico else 0.0
        
        if self.spin_eta_iniziale:
            lotto.eta = self.spin_eta_iniziale.value()

        lotto.clone_assegnato = self.combo_clone.currentText()
        lotto.destinazione_uso = self.combo_destinazione.currentText()

        dati_clone = self.dizionario_cloni.get(lotto.clone_assegnato, {})
        attitudine = dati_clone.get("attitudini", "OPERA")
        if attitudine != "DUAL" and attitudine != lotto.destinazione_uso:
            lotto.moltiplicatore_efficienza_clone = 0.85
        else:
            lotto.moltiplicatore_efficienza_clone = 1.0

        # Ricalcola la biometria iniziale solo se il lotto modificato è ancora fermo prima di partire
        # Evita di azzerare la crescita accumulata durante lo scorrimento del Monitoraggio Real-Time
        if self.parametri.anno_corrente == 1 and self.parametri.stagione_corrente == "Inverno":
            lotto.inizializza_nuovo_ciclo()

        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    def elimina_lotto_selezionato(self):
        # Elimina dalla collezione dei lotti e dalla tabella il lotto selezionato
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe: return

        # Utilizzo del messagggio personalizzato per richiedere la conferma sull'eliminazione del lotto.
        from GUI.utils import mostra_messaggio_stilizzato
        risposta = mostra_messaggio_stilizzato(
            self, 
            "Conferma Eliminazione", 
            "Sei sicuro di voler eliminare permanentemente il lotto selezionato?", 
            "domanda"
        )
        
        # Verifica si l'utente ha premuto "Sì" sul widget
        if risposta == QMessageBox.StandardButton.Yes:
            riga = righe[0].row()
            self.parametri.collezione_lotti.pop(riga)
            self.svuota_e_resetta_interfaccia()
            self.aggiorna_tabella_da_modello()

    def genera_lotto_casuale(self):
        # Funzione che genera in maniera random un lotto da inserire in collezione e nella tabella
        # La funzione creandolo randomicamente potrebbe creare lotti inefficaci per estensione, destinazione commerciale e clone selezionato.
        
        id_progressivo_casuale = self.calcola_prossimo_id_progressivo()
        
        # La superficie casuale è presa randomicamente da un minimo ed un massimo di estensione considerate valide per la gestione
        superficie_casuale = round(random.uniform(0.5, 20.0), 1)

        cloni_disponibili = list(self.dizionario_cloni.keys()) if self.dizionario_cloni else ["I-214", "I-45/51", "Neva", "Velasco"]
        clone_casuale = random.choice(cloni_disponibili)
        destinazione_casuale = random.choice(["OPERA", "INDUSTRIA"])

        sesti_disponibili = ["6x6", "6x5", "7x6", "7x7"]
        sesto_casuale = random.choice(sesti_disponibili)

        lotto_random = Lotto(id_lotto=id_progressivo_casuale, superficie=superficie_casuale)
        lotto_random.sesto_impianto = sesto_casuale
        lati = [float(x) for x in sesto_casuale.split("x")]
        lotto_random.densita_iniziale = int((10000 / (lati[0] * lati[1])) * superficie_casuale)

        lotto_random.indice_attrito_spaziale = random.randint(0, 10)
        lotto_random.indice_tendenza_idrica = round(random.uniform(-1.0, 1.0), 2)

        lotto_random.clone_assegnato = clone_casuale
        lotto_random.destinazione_uso = destinazione_casuale

        dati_clone = self.dizionario_cloni.get(clone_casuale, {})
        attitudine = dati_clone.get("attitudini", "OPERA")
        if attitudine != "DUAL" and attitudine != destinazione_casuale:
            lotto_random.moltiplicatore_efficienza_clone = 0.85
        else:
            lotto_random.moltiplicatore_efficienza_clone = 1.0

        # Impostiamo l'età DOPO l'inizializzazione del ciclo, così il valore randomico persiste
        if self.spin_eta_iniziale:
            lotto_random.eta = random.randint(0, 10)

        # Prepara il nuovo lotto (Evitiamo che sovrascriva l'età casuale)
        lotto_random.inizializza_nuovo_ciclo()

        self.parametri.collezione_lotti.append(lotto_random)
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()
        
    def svuota_e_resetta_interfaccia(self):
        # resettaggio della form quando si spinge il tasto secondario in modalità svuota
        if self.table_lotti: self.table_lotti.clearSelection()
        if self.txt_id_lotto: self.txt_id_lotto.setText(self.calcola_prossimo_id_progressivo())

        if self.spin_ettari: self.spin_ettari.setValue(0.0)
        if self.spin_attrito: self.spin_attrito.setValue(0)
        if self.spin_test_idrico: self.spin_test_idrico.setValue(0.0)
        if self.spin_eta_iniziale: self.spin_eta_iniziale.setValue(0)

        if self.combo_clone and self.combo_clone.count() > 0: self.combo_clone.setCurrentIndex(0)
        if self.combo_sesto_impianto and self.combo_sesto_impianto.count() > 0: self.combo_sesto_impianto.setCurrentIndex(0)
        if self.combo_destinazione and self.combo_destinazione.count() > 0: self.combo_destinazione.setCurrentIndex(0)

        if self.btn_azione: self.btn_azione.setText("Aggiungi Lotto")
        if self.btn_secondario: self.btn_secondario.setText("Svuota")

        self.verifica_coerenza_selvicolturale()

    def esci(self):
        self.close()