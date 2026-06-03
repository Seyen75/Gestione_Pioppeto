
# GUI/form_ditta.py
# Modulo della form di configurazione delle risorse aziendali.
# Sincronizza i dati inseriti con la classe Ditta per impostare i parametri della simulazione.

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from GUI.utils import mostra_messaggio_stilizzato

from Core.ditta import Ditta

class FormDitta(QWidget):
    def __init__(self, ditta_condivisa: Ditta, parametri_condivisi, parent=None):
        super().__init__()

        # Configurazione dei flag della finestra per agganciarla alla form chiamante
        if parent:
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            # Forza la distruzione effettiva della memoria alla chiusura per attivare il segnale .destroyed
            self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Caricamento dinamico dell'interfaccia con QUiLoader
        loader = QUiLoader()
        percorso_ui = os.path.join(os.path.dirname(__file__), "form_ditta.ui")
        self.ui_interfaccia = loader.load(percorso_ui, None)

        # Inserisce la UI dentro il QWidget principale
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui_interfaccia)
        layout.setContentsMargins(10, 10, 10, 10)

        # Salva il riferimento all'oggetto Ditta globale passato alla chiamata e necessario per la gestione dei dati
        self.ditta = ditta_condivisa
        self.parametri = parametri_condivisi # Salviamo il puntatore globale ai parametri della simulazione

        self.setWindowTitle("Inventario Forze di Produzione - Risorse e Flotta")

        # RECUPERO DEI PUNTATORI AI WIDGET

        # Comparto Risorse Umane
        self.spin_operaio_A = self.ui_interfaccia.findChild(object, "spin_operaio_A")
        self.spin_operaio_B = self.ui_interfaccia.findChild(object, "spin_operaio_B")

        # Comparto Flotta Trazione e Manutenzione
        self.spin_trattori_alta = self.ui_interfaccia.findChild(object, "spin_trattori_alta")
        self.spin_trattori_media = self.ui_interfaccia.findChild(object, "spin_trattori_media")
        self.spin_piattaforme = self.ui_interfaccia.findChild(object, "spin_piattaforme")
        self.spin_harvester = self.ui_interfaccia.findChild(object, "spin_harvester")
        self.spin_forwarder = self.ui_interfaccia.findChild(object, "spin_forwarder")
        self.spin_motoseghe = self.ui_interfaccia.findChild(object, "spin_motoseghe")
        self.spin_durata_piano = self.ui_interfaccia.findChild(object, "spin_durata_piano")

        # === COMPARTO FLUIDITÀ E LIMITI ELASTICITÀ DI MERCATO (Nuovi Puntatori PW) ===
        self.dsb_elasticita_spec = self.ui_interfaccia.findChild(object, "dsb_elasticita_spec")
        self.dsb_elasticita_comune = self.ui_interfaccia.findChild(object, "dsb_elasticita_comune")
        self.dsb_elasticita_mezzi_base = self.ui_interfaccia.findChild(object, "dsb_elasticita_mezzi_base")
        self.dsb_elasticita_mezzi_spec = self.ui_interfaccia.findChild(object, "dsb_elasticita_mezzi_spec")

        # Pulsanti di Comando
        self.btn_salva = self.ui_interfaccia.findChild(object, "btn_salva")
        self.btn_esci = self.ui_interfaccia.findChild(object, "btn_esci")

        # INTERFACCIA E SEGNALI
        
        # Inizializza i limiti fisici di sicurezza (min/max) delle DoubleSpinBox di elasticità
        self._configura_limiti_elasticita_ui()
        
        # Pre-popola i widget grafici con i valori correnti salvati nell'oggetto ditta
        self.aggiorna_interfaccia_da_modello()

        if self.btn_salva:
            self.btn_salva.clicked.connect(self.salva_dati_in_modello)

        if self.btn_esci:
            self.btn_esci.clicked.connect(self.esci_form)

        # Centratura geometrica automatica rispetto alla form principale
        if parent:
            self.centra_rispetto_al_parent(parent)

    def _configura_limiti_elasticita_ui(self):
        """Definisce le barriere e gli step di incremento per i moltiplicatori di mercato disaccoppiati."""
        if self.dsb_elasticita_spec:
            self.dsb_elasticita_spec.setMinimum(1.0)
            self.dsb_elasticita_spec.setMaximum(2.5)
            self.dsb_elasticita_spec.setSingleStep(0.1)
            self.dsb_elasticita_spec.setDecimals(1)
            
        if self.dsb_elasticita_comune:
            self.dsb_elasticita_comune.setMinimum(1.0)
            self.dsb_elasticita_comune.setMaximum(5.0)
            self.dsb_elasticita_comune.setSingleStep(0.5)
            self.dsb_elasticita_comune.setDecimals(1)
            
        if self.dsb_elasticita_mezzi_base:
            self.dsb_elasticita_mezzi_base.setMinimum(1.0)
            self.dsb_elasticita_mezzi_base.setMaximum(4.0)
            self.dsb_elasticita_mezzi_base.setSingleStep(0.5)
            self.dsb_elasticita_mezzi_base.setDecimals(1)
            
        if self.dsb_elasticita_mezzi_spec:
            self.dsb_elasticita_mezzi_spec.setMinimum(1.0)
            self.dsb_elasticita_mezzi_spec.setMaximum(3.0)
            self.dsb_elasticita_mezzi_spec.setSingleStep(0.5)
            self.dsb_elasticita_mezzi_spec.setDecimals(1)

    def aggiorna_interfaccia_da_modello(self):
        # Estrae i valori reali dall'oggetto ditta e popola gli SpinBox grafici
        if self.spin_operaio_A: self.spin_operaio_A.setValue(self.ditta.operai_grado_A)
        if self.spin_operaio_B: self.spin_operaio_B.setValue(self.ditta.operai_grado_B)
        
        if self.spin_trattori_alta: self.spin_trattori_alta.setValue(self.ditta.trattori_alta_potenza)
        if self.spin_trattori_media: self.spin_trattori_media.setValue(self.ditta.trattori_media_potenza)
        if self.spin_piattaforme: self.spin_piattaforme.setValue(self.ditta.piattaforme_aeree_semoventi)
        if self.spin_harvester: self.spin_harvester.setValue(self.ditta.harvester_abbattitori)
        if self.spin_forwarder: self.spin_forwarder.setValue(self.ditta.forwarder_caricatori)
        if self.spin_motoseghe: self.spin_motoseghe.setValue(self.ditta.kit_motoseghe_professionali)
        if self.spin_durata_piano: self.spin_durata_piano.setValue(self.parametri.anni_durata_target)

        # Allineamento dei valori correnti dei moltiplicatori di elasticità disaccoppiati
        elasti = getattr(self.ditta, "moltiplicatori_elasticita", {})
        if self.dsb_elasticita_spec and "personale_spec" in elasti:
            self.dsb_elasticita_spec.setValue(elasti["personale_spec"])
        if self.dsb_elasticita_comune and "personale_comune" in elasti:
            self.dsb_elasticita_comune.setValue(elasti["personale_comune"])
        if self.dsb_elasticita_mezzi_base and "mezzi_base" in elasti:
            self.dsb_elasticita_mezzi_base.setValue(elasti["mezzi_base"])
        if self.dsb_elasticita_mezzi_spec and "mezzi_spec" in elasti:
            self.dsb_elasticita_mezzi_spec.setValue(elasti["mezzi_spec"])

    def salva_dati_in_modello(self):
        # Legge i valori impostati dall'utente e aggiorna l'istanza della ditta se i controlli di consistenza sono passati
        op_A = self.spin_operaio_A.value() if self.spin_operaio_A else 0
        op_B = self.spin_operaio_B.value() if self.spin_operaio_B else 0

        if (op_A + op_B) == 0:
            mostra_messaggio_stilizzato(
                            self, 
                            "Inconsistenza Organico", 
                            "Impossibile salvare: la ditta deve disporre di almeno un lavoratore per operare nei cantieri.", 
                            "avviso"
                        )
            return

        if self.spin_operaio_A: self.ditta.operai_grado_A = op_A
        if self.spin_operaio_B: self.ditta.operai_grado_B = op_B
        
        if self.spin_trattori_alta: self.ditta.trattori_alta_potenza = self.spin_trattori_alta.value()
        if self.spin_trattori_media: self.ditta.trattori_media_potenza = self.spin_trattori_media.value()
        if self.spin_piattaforme: self.ditta.piattaforme_aeree_semoventi = self.spin_piattaforme.value()
        if self.spin_harvester: self.ditta.harvester_abbattitori = self.spin_harvester.value()
        if self.spin_forwarder: self.ditta.forwarder_caricatori = self.spin_forwarder.value()
        if self.spin_motoseghe: self.ditta.kit_motoseghe_professionali = self.spin_motoseghe.value()
        
        # Salvataggio delle nuove impostazioni di elasticità disaccoppiata inserite dall'utente
        if hasattr(self.ditta, "moltiplicatori_elasticita"):
            if self.dsb_elasticita_spec:
                self.ditta.moltiplicatori_elasticita["personale_spec"] = self.dsb_elasticita_spec.value()
            if self.dsb_elasticita_comune:
                self.ditta.moltiplicatori_elasticita["personale_comune"] = self.dsb_elasticita_comune.value()
            if self.dsb_elasticita_mezzi_base:
                self.ditta.moltiplicatori_elasticita["mezzi_base"] = self.dsb_elasticita_mezzi_base.value()
            if self.dsb_elasticita_mezzi_spec:
                self.ditta.moltiplicatori_elasticita["mezzi_spec"] = self.dsb_elasticita_mezzi_spec.value()

        # Salva la durata target degli anni all'interno della configurazione globale parametri
        if self.spin_durata_piano: self.parametri.anni_durata_target = self.spin_durata_piano.value()

        # Sincronizzazione immediata del monte ore stagionale nominale con il nuovo organico salvato
        if hasattr(self.ditta, "inizializza_serbatoi_stagionali"):
            self.ditta.inizializza_serbatoi_stagionali(55)
        else:
            ore_ricalcolate = (self.ditta.operai_grado_A + self.ditta.operai_grado_B) * 450.0
            self.ditta.serbatoi_ore = {
                "Inverno": ore_ricalcolate, "Primavera": ore_ricalcolate, "Estate": ore_ricalcolate, "Autunno": ore_ricalcolate
            }

        self.close()

    def centra_rispetto_al_parent(self, parent):
        # Posiziona la form al centro esatto della form padre
        geometria_parent = parent.geometry()
        
        # dimensioni della finestra per il calcolo e il rendering (altezza modificata a 350 per contenere i nuovi controlli)
        larghezza_self = 686
        altezza_self = 406

        # Calcolo geometrico della mezzeria rispetto alla form principale
        x = geometria_parent.x() + (geometria_parent.width() - larghezza_self) // 2
        y = geometria_parent.y() + (geometria_parent.height() - altezza_self) // 2
        
        self.setFixedSize(larghezza_self, altezza_self)
        self.move(x, y)

    def esci_form(self):
        self.close()