
# Modulo Finestra principale (Dashboard) del simulatore di pioppicoltura.
# Gestisce i flussi di lavoro, il caricamento dinamico della UI e gli stati della barra delle applicazioni.

import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QGraphicsDropShadowEffect, QMessageBox, QApplication, QProgressDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from GUI.utils import mostra_messaggio_stilizzato

# Importazione delle risorse del Core
from Core.gestori_clone import GestoreCloni
from Core.ditta import Ditta
from Core.parametri_simulazione import ParametriSimulazione
from Core.SimulatorePioppicultura import SimulatorePioppicoltura
from Core.lotto import Lotto

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

        # IMPOSTAZIONE PROFILO STANDARD DI DEFAULT PER LA DITTA (Medio-Grande Bilanciata)
        self.ditta_attiva.operai_grado_A = 1
        self.ditta_attiva.operai_grado_B = 2
        self.ditta_attiva.trattori_alta_potenza = 1
        self.ditta_attiva.trattori_media_potenza = 1
        self.ditta_attiva.piattaforme_aeree_semoventi = 1
        self.ditta_attiva.harvester_abbattitori = 1
        self.ditta_attiva.forwarder_caricatori = 1
        self.ditta_attiva.kit_motoseghe_professionali = 2
        self.ditta_attiva.coefficiente_iufro = 0.80
        
        # Inizializzazione del monte ore stagionale iniziale (3 operai * 450 ore = 1350 ore)
        ore_standard = (self.ditta_attiva.operai_grado_A + self.ditta_attiva.operai_grado_B) * 450.0
        self.ditta_attiva.serbatoi_ore = {
            "Inverno": ore_standard,
            "Primavera": ore_standard,
            "Estate": ore_standard,
            "Autunno": ore_standard
        }

        # Orizzonte temporale di default per lo scenario di assestamento standard (10 Anni)
        self.parametri_condivisi.anni_durata_target = 10

        # IMPOSTAZIONE PIANO DI ASSESTAMENTO DI DEFAULT (Fustaia Disetanea Coerente sui 3 Output)
        # 10 lotti da 3.0 ettari ciascuno, alternati per destinazione d'uso ed età (0-9 anni)
        configurazione_lotti_default = [
            {"id": "LTI-001", "clone": "I-214", "dest": "OPERA", "eta": 9, "idrico": 0.0},
            {"id": "LTI-002", "clone": "Velasco", "dest": "INDUSTRIA", "eta": 8, "idrico": 0.2},
            {"id": "LTI-003", "clone": "Neva", "dest": "OPERA", "eta": 7, "idrico": -0.4},
            {"id": "LTI-004", "clone": "I-45/51", "dest": "INDUSTRIA", "eta": 6, "idrico": 0.0},
            {"id": "LTI-005", "clone": "I-214", "dest": "OPERA", "eta": 5, "idrico": 0.1},
            {"id": "LTI-006", "clone": "Velasco", "dest": "INDUSTRIA", "eta": 4, "idrico": 0.2},
            {"id": "LTI-007", "clone": "Neva", "dest": "OPERA", "eta": 3, "idrico": -0.2},
            {"id": "LTI-008", "clone": "I-45/51", "dest": "INDUSTRIA", "eta": 2, "idrico": 0.0},
            {"id": "LTI-009", "clone": "I-214", "dest": "OPERA", "eta": 1, "idrico": 0.0},
            {"id": "LTI-010", "clone": "Velasco", "dest": "INDUSTRIA", "eta": 0, "idrico": 0.3}
        ]

        self.parametri_condivisi.collezione_lotti = []
        for conf in configurazione_lotti_default:
            lotto = Lotto(id_lotto=conf["id"], superficie=3.0)
            lotto.sesto_impianto = "6x6"
            lotto.clone_assegnato = conf["clone"]
            lotto.destinazione_uso = conf["dest"]
            lotto.indice_attrito_spaziale = 2
            lotto.indice_tendenza_idrica = conf["idrico"]
            lotto.densita_iniziale = int((10000 / (6 * 6)) * 3.0)
            lotto.eta = conf["eta"]  # Inietta la classe d'età sfalsata
            lotto.moltiplicatore_efficiency_clone = 1.0
            lotto.inizializza_nuovo_ciclo() # Calcola la biometria retroattiva di partenza
            self.parametri_condivisi.collezione_lotti.append(lotto)

        # RECUPERO WIDGETS E COLLEGAMENTO AZIONI
        btn_esci = widget_centrale.findChild(QPushButton, "btn_esci")
        self.btn_ditta = widget_centrale.findChild(QPushButton, "btn_gestione_ditta")
        self.btn_lotti = widget_centrale.findChild(QPushButton, "btn_gestione_lotti")
        self.btn_simulazione = widget_centrale.findChild(QPushButton, "btn_simulazione")
        self.btn_monitoraggio = widget_centrale.findChild(QPushButton, "btn_monitoraggio")
        self.btn_valutazioni = widget_centrale.findChild(QPushButton, "btn_valutazioni")
        self.btn_reset = widget_centrale.findChild(QPushButton, "btn_reset")

        # Collegamento dei PushButton con i relativi metodi
        if btn_esci: btn_esci.clicked.connect(QApplication.instance().quit)
        if self.btn_ditta: self.btn_ditta.clicked.connect(self.ditta)
        if self.btn_lotti: self.btn_lotti.clicked.connect(self.lotti)
        if self.btn_simulazione: self.btn_simulazione.clicked.connect(self.simulazione)
        if self.btn_monitoraggio: self.btn_monitoraggio.clicked.connect(self.monitoraggio)
        if self.btn_valutazioni: self.btn_valutazioni.clicked.connect(self.valutazione)
        if self.btn_reset: self.btn_reset.clicked.connect(self.ripristina_simulazione_globale)

        # GRAFICA DELLA FORM 
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
        ditta_pronta = (self.ditta_attiva.operai_grado_A + self.ditta_attiva.operai_grado_B) > 0
        lotti_pronti = len(self.parametri_condivisi.collezione_lotti) > 0
    
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
    
        elif ditta_pronta and lotti_pronti and not self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(True)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(True)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(False)
            self.statusBar().showMessage("✅ Sistema pronto. Scegliere 'Avvia Simulazione' (Batch) o 'Monitoraggio Real-Time' (Passo-Passo).")
    
        elif self.simulazione_eseguita:
            if self.btn_simulazione: self.btn_simulazione.setEnabled(False)
            if self.btn_monitoraggio: self.btn_monitoraggio.setEnabled(False)
            if self.btn_valutazioni: self.btn_valutazioni.setEnabled(True)
            self.statusBar().showMessage("📊 Simulazione conclusa! Analisi diagnostica disponibili in 'Report Finale'.")

    def ripristina_simulazione_globale(self):
        """Azione collegata al pulsante 'Reset'."""
        risposta = mostra_messaggio_stilizzato(
            parent=self, titolo="Conferma Ripristino",
            testo="Sei sicuro di voler azzerare la simulazione corrente?\nI dati storici e le rese andranno persi.",
            tipo="domanda"
        )
        if risposta != QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage("🔄 Operazione di ripristino annullata.")
            return
    
        self.parametri_condivisi.reset_simulazione_globale()
        
        if hasattr(self.ditta_attiva, "ripristina_serbatoi_nominali"):
            self.ditta_attiva.ripristina_serbatoi_nominali()
        else:
            ore_standard = (self.ditta_attiva.operai_grado_A + self.ditta_attiva.operai_grado_B) * 450.0
            self.ditta_attiva.serbatoi_ore = {
                "Inverno": ore_standard, "Primavera": ore_standard, "Estate": ore_standard, "Autunno": ore_standard
            }
        
        self.simulazione_eseguita = False
        self.aggiorna_stato_interfaccia()
        self.statusBar().showMessage("🔄 Sistema resettato. Registri storici azzerati.")

    def ditta(self):
        print("Avvio finestra gestione ditta")
        # AGGIORNATO: Passiamo ditta_attiva E parametri_condivisi
        self.finestra_ditta = FormDitta(self.ditta_attiva, self.parametri_condivisi, self)

        # Finestra avviata como modale per evitare che la form padre possa essere utilizzata erroneamente mentre si inseriscono i dati
        from PySide6.QtCore import Qt
        self.finestra_ditta.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.finestra_ditta.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_ditta.show()

    def lotti(self):
        self.finestra_lotti = FormLotti(self.parametri_condivisi, self)
        self.finestra_lotti.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.finestra_lotti.destroyed.connect(self.aggiorna_stato_interfaccia)
        self.finestra_lotti.show()

    def simulazione(self):
        self.statusBar().showMessage("Inizializzazione del calcolo forestale in corso...")
        self.parametri_condivisi.reset_simulazione_globale()

        # Configura la barra di avanzamento basata sugli ANNI di durata target, non sulla conclusione dei lotti!
        progress = QProgressDialog("Inizializzazione del motore forestale...", "Annulla", 0, self.parametri_condivisi.anni_durata_target, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setWindowTitle("Elaborazione Scenario")
        progress.setMinimumDuration(0)
        progress.setAutoClose(True)

        try:
            motore = SimulatorePioppicoltura(self.ditta_attiva, self.parametri_condivisi)
            fine_scatto = False
            
            while not fine_scatto:
                if progress.wasCanceled():
                    self.statusBar().showMessage("🔄 Simulazione interrotta.")
                    return

                # Il simulatore avanza di un trimestre e restituisce se il tempo è scaduto
                stato_tempo = motore.avanza_passo_simulazione()
                fine_scatto = stato_tempo["simulazione_terminata"]
                
                anno = self.parametri_condivisi.anno_corrente
                stagione = self.parametri_condivisi.stagione_corrente
                
                progress.setLabelText(f"Elaborazione Anno {anno} - {stagione} | Assestamento continuo...")
                progress.setValue(min(anno, self.parametri_condivisi.anni_durata_target))
                QApplication.processEvents()

            self.simulazione_eseguita = True
            mostra_messaggio_stilizzato(
                parent=self, titolo="Simulazione Conclusa",
                testo=f"Il piano di assestamento su {self.parametri_condivisi.anni_durata_target} anni è stato completato.\nI tre output sono pronti.",
                tipo="info"
            )
            
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Errore di Calcolo", f"Crash nel motore:\n{str(e)}")
            self.simulazione_eseguita = False

        self.aggiorna_stato_interfaccia()

    def monitoraggio(self):
        # PROSSIMO PASSO DA SVILUPPARE
        print("Avvio finestra monitoraggio")

    def valutazione(self):
        print("Avvio finestra valutazione")