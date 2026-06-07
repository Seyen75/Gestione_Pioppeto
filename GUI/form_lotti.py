# Modulo per il pannello di controllo e pianificazione del pioppeto.
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

        if self.table_lotti:
            self.table_lotti.setShowGrid(True)
            self.table_lotti.setColumnCount(6)
            
            orizzontale_header = self.table_lotti.horizontalHeader()
            orizzontale_header.setSectionResizeMode(orizzontale_header.ResizeMode.Interactive)
            
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

        self.btn_azione = self.ui_interfaccia.findChild(object, "btn_azione_lotto")
        self.btn_secondario = self.ui_interfaccia.findChild(object, "btn_elimina_lotto")
        self.btn_randomizza = self.ui_interfaccia.findChild(object, "btn_randomizza")
        self.btn_esci = self.ui_interfaccia.findChild(object, "btn_esci")

        if self.txt_id_lotto:
            self.txt_id_lotto.setReadOnly(True)

        if self.btn_azione: self.btn_azione.clicked.connect(self.gestisci_azione_pulsante_principale)
        if self.btn_secondario: self.btn_secondario.clicked.connect(self.gestisci_azione_pulsante_secondario)
        if self.btn_randomizza: self.btn_randomizza.clicked.connect(self.genera_lotto_casuale)
        if self.btn_esci: self.btn_esci.clicked.connect(self.esci)
        
        if self.table_lotti:
            self.table_lotti.itemSelectionChanged.connect(self.carica_lotto_selezionato)
            self.table_lotti.setSelectionBehavior(self.table_lotti.SelectionBehavior.SelectRows)
            self.table_lotti.setSelectionMode(self.table_lotti.SelectionMode.SingleSelection)

        if self.combo_clone: self.combo_clone.currentTextChanged.connect(self.verifica_coerenza_selvicolturale)
        if self.combo_destinazione: self.combo_destinazione.currentTextChanged.connect(self.verifica_coerenza_selvicolturale)

        self.popola_cloni_disponibili()
        self.popola_sesti_disponibili()
        self.popola_destinazioni_disponibili()
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    # Funzione che chiude la form dei lotti, notificando alla finestra padre di aggiornare lo stato dell'interfaccia principale per riflettere eventuali modifiche ai lotti, e poi chiudendo la finestra figlia

    def showEvent(self, event):
        super().showEvent(event)
        parent = self.parentWidget()
        if parent:
            geometria_parent = parent.geometry()
            larghezza_self, altezza_self = 647, 720
            x = geometria_parent.x() + (geometria_parent.width() - larghezza_self) // 2
            y = geometria_parent.y() + (geometria_parent.height() - altezza_self) // 2
            self.move(x, y)

    # Funzione che si attiva quando la form viene chiusa, notificando alla finestra padre di aggiornare lo stato dell'interfaccia principale 
    # per riflettere eventuali modifiche ai lotti
        
    def closeEvent(self, event):
        parent = self.parentWidget()
        if parent and hasattr(parent, "aggiorna_stato_interfaccia"):
            parent.aggiorna_stato_interfaccia()
        super().closeEvent(event)

    # Funzione che popola la combo box dei cloni disponibili leggendo da un file JSON esterno, con fallback a dati hardcoded se il file non esiste o è malformato

    def popola_cloni_disponibili(self):
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
            self.dizionario_cloni = {
                "I-214": {"attitudini": "OPERA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.85}},
                "I-45/51": {"attitudini": "INDUSTRIA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.90}},
                "Neva": {"attitudini": "OPERA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.88}},
                "Velasco": {"attitudini": "INDUSTRIA", "proprieta_tecnologiche": {"densita_verde_t_m3": 0.92}}
            }
            self.combo_clone.addItems(list(self.dizionario_cloni.keys()))

    # Funzione che popola la combo box dei sesti d'impianto disponibili con opzioni predefinite, permettendo all'utente di scegliere tra configurazioni standard di piantagione

    def popola_sesti_disponibili(self):
        if not self.combo_sesto_impianto: return
        self.combo_sesto_impianto.clear()
        self.combo_sesto_impianto.addItems(["6x6", "6x5", "7x6", "7x7"])

    # Funzione che popola la combo box delle destinazioni d'uso disponibili con opzioni predefinite, permettendo all'utente di specificare se il lotto è destinato a biomassa/cartiera o a compensati di pregio

    def popola_destinazioni_disponibili(self):
        if not self.combo_destinazione: return
        self.combo_destinazione.clear()
        self.combo_destinazione.addItems(["OPERA", "INDUSTRIA"])

    # Funzione che verifica la coerenza selvicolturale tra il clone selezionato e la destinazione d'uso scelta, mostrando un messaggio di avviso se l'abbinamento non è ottimale e spiegando i potenziali rischi o inefficienze derivanti da una scelta non coerente

    def verifica_coerenza_selvicolturale(self):
        if not self.combo_clone or not self.combo_destinazione or not self.lbl_avviso_clone:
            return
        clone_scelto = self.combo_clone.currentText()
        destinazione_scelta = self.combo_destinazione.currentText().upper().strip()

        mappatura_attitudini_cloni = {
            "I-214": "OPERA", "Neva": "OPERA", "I-45/51": "INDUSTRIA", "Velasco": "INDUSTRIA", "AF2": "INDUSTRIA"
        }
       
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

    # Funzione che calcola il prossimo ID progressivo per un nuovo lotto basandosi sul numero di lotti già presenti nella collezione, restituendo una stringa formattata con prefisso e numerazione a tre cifre

    def calcola_prossimo_id_progressivo(self) -> str:
        return f"LTI-{len(self.parametri.collezione_lotti) + 1:03d}"

    # Funzione che aggiorna la tabella dei lotti visualizzata nell'interfaccia grafica, leggendo i dati attuali dalla collezione di lotti nei parametri condivisi e popolando ogni riga con le informazioni chiave di ciascun lotto, formattando i valori in modo leggibile e allineando il testo al centro per una migliore estetica

    def aggiorna_tabella_da_modello(self):
        if not self.table_lotti: 
            return
        
        lotti = self.parametri.collezione_lotti
        self.table_lotti.setRowCount(len(lotti))
        
        for riga, lotto in enumerate(lotti):
            dati = [
                str(lotto.id_lotto),
                f"{lotto.superficie_ettari:.2f} ha",
                str(lotto.clone_assegnato),
                str(lotto.sesto_impianto),
                f"{lotto.eta} anni",
                str(lotto.destinazione_uso)
            ]
            
            for colonna, valore in enumerate(dati):
                item = QTableWidgetItem(valore)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Opzionale: rendiamo le celle non modificabili dall'utente
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_lotti.setItem(riga, colonna, item)

    # Funzione che valida i dati di input inseriti dall'utente nei widget grafici prima di aggiungere o modificare un lotto, controllando che la superficie sia non eccessivamente grande, restituendo True se i dati sono validi o mostrando un messaggio di errore e restituendo False se i dati non sono accettabili

    def valida_dati_input(self) -> bool:
        ettari = self.spin_ettari.value()
        if ettari > 100.0:
            mostra_messaggio_stilizzato(self, "Errore Critico", "Superficie fuori scala per singolo lotto (>100 ha).", "critico")
            return False
        return True

    # Funzione che gestisce l'azione del pulsante principale, decidendo se aggiungere un nuovo lotto o salvare le modifiche a un lotto esistente in base al testo attuale del pulsante, e chiamando la funzione appropriata per eseguire l'operazione desiderata

    def gestisci_azione_pulsante_principale(self):
        if self.btn_azione.text() == "Aggiungi Lotto":
            self.aggiungi_nuovo_lotto()
        else:
            self.salva_modifica_lotto()

    # Funzione che gestisce l'azione del pulsante secondario, decidendo se svuotare e resettare l'interfaccia per prepararla all'inserimento di un nuovo lotto o eliminare il lotto attualmente selezionato in base al testo attuale del pulsante, e chiamando la funzione appropriata per eseguire l'operazione desiderata

    def gestisci_azione_pulsante_secondario(self):
        if self.btn_secondario.text() == "Svuota":
            self.svuota_e_resetta_interfaccia()
        else:
            self.elimina_lotto_selezionato()

    # Funzione che aggiunge un nuovo lotto alla collezione basandosi sui dati inseriti dall'utente nei widget grafici, creando un'istanza di Lotto con i parametri strutturali e dinamici specificati, calcolando la densità iniziale in base al sesto d'impianto scelto, valutando la coerenza selvicolturale per assegnare un moltiplicatore di efficienza clone, inizializzando il ciclo biologico del lotto e aggiornando l'interfaccia grafica per riflettere la nuova aggiunta

    def aggiungi_nuovo_lotto(self):
        if not self.valida_dati_input(): return

        id_confermato = self.txt_id_lotto.text()
        nuovo_lotto = Lotto(id_lotto=id_confermato, superficie=self.spin_ettari.value())

        nuovo_lotto.sesto_impianto = self.combo_sesto_impianto.currentText()
        lati = [float(x) for x in nuovo_lotto.sesto_impianto.split("x")]
        nuovo_lotto.densita_iniziale = int((10000 / (lati[0] * lati[1])))

        nuovo_lotto.indice_attrito_spaziale = int(self.spin_attrito.value()) if self.spin_attrito else 0
        nuovo_lotto.indice_tendenza_idrica = float(self.spin_test_idrico.value()) if self.spin_test_idrico else 0.0
        
        if self.spin_eta_iniziale:
            nuovo_lotto.eta = self.spin_eta_iniziale.value()
            
        nuovo_lotto.clone_assegnato = self.combo_clone.currentText()
        nuovo_lotto.destinazione_uso = self.combo_destinazione.currentText()

        dati_clone = self.dizionario_cloni.get(nuovo_lotto.clone_assegnato, {})
        attitudine = dati_clone.get("attitudini", "OPERA")
        if attitudine != "DUAL" and attitudine != nuovo_lotto.destinazione_uso:
            nuovo_lotto.moltiplicatore_efficienza_clone = 0.85
        else:
            nuovo_lotto.moltiplicatore_efficienza_clone = 1.0

        nuovo_lotto.inizializza_nuovo_ciclo()
        self.parametri.collezione_lotti.append(nuovo_lotto)
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    # Funzione che carica i dati del lotto attualmente selezionato nella tabella dei lotti e li visualizza nei widget grafici per permettere all'utente di visualizzare e modificare le informazioni del lotto, aggiornando anche il testo dei pulsanti per riflettere lo stato di modifica

    def carica_lotto_selezionato(self):
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe: return

        riga = righe[0].row()
        lotto = self.parametri.collezione_lotti[riga]

        self.txt_id_lotto.setText(lotto.id_lotto)
        self.spin_ettari.setValue(lotto.superficie_ettari)

        if self.spin_attrito: self.spin_attrito.setValue(lotto.indice_attrito_spaziale)
        if self.spin_test_idrico: self.spin_test_idrico.setValue(lotto.indice_tendenza_idrica)

        if self.spin_eta_iniziale: self.spin_eta_iniziale.setValue(lotto.eta)

        index_clone = self.combo_clone.findText(lotto.clone_assegnato)
        if index_clone >= 0: self.combo_clone.setCurrentIndex(index_clone)

        index_sesto = self.combo_sesto_impianto.findText(lotto.sesto_impianto)
        if index_sesto >= 0: self.combo_sesto_impianto.setCurrentIndex(index_sesto)

        index_dest = self.combo_destinazione.findText(lotto.destinazione_uso)
        if index_dest >= 0: self.combo_destinazione.setCurrentIndex(index_dest)

        self.btn_azione.setText("Aggiorna")
        self.btn_secondario.setText("Elimina")

    # Funzione che salva le modifiche apportate a un lotto esistente basandosi sui dati inseriti dall'utente nei widget grafici, aggiornando i parametri strutturali e dinamici del lotto selezionato, ricalcolando la densità iniziale se il sesto d'impianto è stato modificato, valutando nuovamente la coerenza selvicolturale per aggiornare il moltiplicatore di efficienza clone, e aggiornando l'interfaccia grafica per riflettere le modifiche salvate

    def salva_modifica_lotto(self):
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe or not self.valida_dati_input(): return

        riga = righe[0].row()
        lotto = self.parametri.collezione_lotti[riga]

        # Memorizza le vecchie dimensioni per calcolare la proporzione
        vecchie_piante_teoriche = lotto.superficie_ettari * lotto.densita_iniziale

        # Aggiorna i parametri strutturali
        lotto.superficie_ettari = self.spin_ettari.value()
        lotto.sesto_impianto = self.combo_sesto_impianto.currentText()
        lati = [float(x) for x in lotto.sesto_impianto.split("x")]
        
        lotto.densita_iniziale = int(10000 / (lati[0] * lati[1]))

        # RICALCOLO DINAMICO DELLE PIANTE E DEI VOLUMI
        nuove_piante_teoriche = lotto.superficie_ettari * lotto.densita_iniziale
        
        if vecchie_piante_teoriche > 0:
            # Calcola di quanto è aumentata/diminuita l'area o la densità
            fattore_scala = nuove_piante_teoriche / vecchie_piante_teoriche
            
            # Scala gli alberi vivi mantenendo la percentuale di mortalità già subita
            lotto.numero_piante_vive = int(lotto.numero_piante_vive * fattore_scala)
            
            # Se si modifica a simulazione già avviata, aggiorna la cache in tempo reale
            if hasattr(lotto, "dati_correnti") and "volume_singolo_m3" in lotto.dati_correnti:
                lotto.dati_correnti["piante_attive"] = lotto.numero_piante_vive
                lotto.dati_correnti["volume_totale_m3"] = round(lotto.dati_correnti["volume_singolo_m3"] * lotto.numero_piante_vive, 2)
        else:
            # Fallback di sicurezza se il lotto è a 0
            lotto.numero_piante_vive = int(nuove_piante_teoriche)

        # Aggiorna gli altri attributi
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

        if self.parametri.anno_corrente == 1 and self.parametri.stagione_corrente == "Inverno":
            lotto.inizializza_nuovo_ciclo()

        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()

    # Funzione che elimina il lotto attualmente selezionato nella tabella dei lotti, chiedendo conferma all'utente prima di procedere con l'eliminazione permanente, e aggiornando l'interfaccia grafica per riflettere la rimozione del lotto

    def elimina_lotto_selezionato(self):
        righe = self.table_lotti.selectionModel().selectedRows()
        if not righe: return

        risposta = mostra_messaggio_stilizzato(
            self, "Conferma Eliminazione", "Sei sicuro di voler eliminare permanentemente il lotto selezionato?", "domanda"
        )
        if risposta == QMessageBox.StandardButton.Yes:
            riga = righe[0].row()
            self.parametri.collezione_lotti.pop(riga)
            self.svuota_e_resetta_interfaccia()
            self.aggiorna_tabella_da_modello()

    # Funzione che genera un lotto casuale con parametri randomizzati all'interno di range accettabili, permettendo di popolare rapidamente la collezione di lotti per test o simulazioni, e aggiornando l'interfaccia grafica per riflettere la nuova aggiunta

    def genera_lotto_casuale(self):
        id_progressivo_casuale = self.calcola_prossimo_id_progressivo()
        superficie_casuale = round(random.uniform(0.5, 20.0), 1)

        cloni_disponibili = list(self.dizionario_cloni.keys()) if self.dizionario_cloni else ["I-214", "I-45/51", "Neva", "Velasco"]
        clone_casuale = random.choice(cloni_disponibili)
        destinazione_casuale = random.choice(["OPERA", "INDUSTRIA"])
        sesto_casuale = random.choice(["6x6", "6x5", "7x6", "7x7"])

        lotto_random = Lotto(id_lotto=id_progressivo_casuale, superficie=superficie_casuale)
        lotto_random.sesto_impianto = sesto_casuale
        lati = [float(x) for x in sesto_casuale.split("x")]
        lotto_random.densita_iniziale = int(10000 / (lati[0] * lati[1]))
        
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

        # --- CORRETTO: Iniezione dell'età nativa prima del ciclo ---
        lotto_random.eta = random.randint(0, 10)
        lotto_random.inizializza_nuovo_ciclo()

        self.parametri.collezione_lotti.append(lotto_random)
        self.svuota_e_resetta_interfaccia()
        self.aggiorna_tabella_da_modello()
    
    # Funzione che svuota e resetta i widget grafici dell'interfaccia, riportandoli ai valori di default o al prossimo ID progressivo disponibile, e aggiornando il testo dei pulsanti per preparare l'interfaccia all'inserimento di un nuovo lotto o alla visualizzazione dello stato iniziale
        
    def svuota_e_resetta_interfaccia(self):
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