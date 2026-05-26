# Core/ditta.py
# Modulo Rappresentazione della ditta forestale.
# Gestisce l'inventario delle risorse, i serbatoi d'ore stagionali e la diagnostica dei colli di bottiglia.

class Ditta:
    def __init__(self, nome: str = "Azienda Pioppicola Padana"):
        # ANAGRAFICA E PARAMETRI GENERALI
        self.nome_ditta: str = nome
        self.ore_giorno_standard: int = 8
        self.coefficiente_rendimento_cantiere: float = 0.80  # Adeguamento per Normativa IUFRO (20% tempi accessori) - Da indicare in PW
        self.coefficiente_iufro: float = 0.80              

        # FORZA LAVORO
        self.operai_grado_A: int = 0  # Specializzati (Conduttori macchine complesse/Motoseghisti avanzati)
        self.operai_grado_B: int = 0  # Generici (Manovali a terra, supporto impianti)

        # PARCO MACCHINE E STRUMENTAZIONI
        self.trattori_alta_potenza: int = 0         # >150 CV (Scasso/Impianto)
        self.trattori_media_potenza: int = 0        # 80-110 CV (Interfilari/Trattamenti)
        self.piattaforme_aeree_semoventi: int = 0   # Ragni elevatori per potatura alta
        self.harvester_abbattitori: int = 0         # Abbattitori pioppicoli a testa rotante
        self.forwarder_caricatori: int = 0          # Caricatori forestali pesanti con ralle
        self.kit_motoseghe_professionali: int = 0   # Per cantiere abbattimento tradizionale

        # DIZIONARIO CENTRALIZZATO UNICO DEI SERBATOI ORE (Struttura Master)
        self.serbatoi_ore = {
            "grado_A": 0.0,
            "grado_B": 0.0,
            "trattori_alta": 0.0,
            "trattori_media": 0.0,
            "piattaforme": 0.0,
            "harvester": 0.0,
            "forwarder": 0.0,
            "motoseghe": 0.0
        }

        # Sincronizziamo anche le variabili singole nominali per retrocompatibilità assoluta con la GUI
        self.serbatoio_ore_grado_A: float = 0.0
        self.serbatoio_ore_grado_B: float = 0.0
        self.serbatoio_ore_trattori_alta: float = 0.0
        self.serbatoio_ore_trattori_media: float = 0.0
        self.serbatoio_ore_piattaforme: float = 0.0
        self.serbatoio_ore_harvester: float = 0.0
        self.serbatoio_ore_forwarder: float = 0.0
        self.serbatoio_ore_motoseghe: float = 0.0

        # LISTA PRESTAZIONALI UNITARIE (Abaco IUFRO interno)
        self.prestazioni_macchine = {
            "impianto": {
                "ha_ora_per_linea": 0.04,
                "squadra": {"grado_A": 1, "grado_B": 1, "trattori_alta": 1}
            },
            "trinciatura": {
                "ha_ora_per_linea": 0.30,
                "squadra": {"grado_A": 1, "grado_B": 0, "trattori_media": 1}
            },
            "potatura": {
                "ha_ora_per_linea": 0.08,
                "squadra": {"grado_A": 1, "grado_B": 1, "piattaforme": 1}
            },
            "raccolta_tradizionale": {
                "m3_ora_per_linea": 2.5,
                "squadra": {"grado_A": 2, "grado_B": 0, "motoseghe": 1, "trattori_media": 1}
            },
            "raccolta_avanzata": {
                "m3_ora_per_linea": 12.0,
                "squadra": {"grado_A": 2, "grado_B": 0, "harvester": 1, "forwarder": 1}
            }
        }

        # REGISTRI DI UTILIZZO E LOGISTICA TOTALI
        self.ore_lavoro_effettivo: float = 0.0
        self.ore_logistica_trasferta: float = 0.0 

        # CONTATORI DI FALLIMENTO DIAGNOSTICI
        self.fallimenti_grado_A: int = 0
        self.fallimenti_grado_B: int = 0
        self.fallimenti_trattori_alta: int = 0
        self.fallimenti_trattori_media: int = 0
        self.fallimenti_piattaforme: int = 0
        self.fallimenti_harvester: int = 0
        self.fallimenti_forwarder: int = 0
        self.fallimenti_motoseghe: int = 0

    def configura_risorse(self, op_A: int, op_B: int, t_alta: int, t_media: int,
                          piattaforme: int, harvester: int, forwarder: int, motoseghe: int):
        self.operai_grado_A = max(0, op_A)
        self.operai_grado_B = max(0, op_B)
        self.trattori_alta_potenza = max(0, t_alta)
        self.trattori_media_potenza = max(0, t_media)
        self.piattaforme_aeree_semoventi = max(0, piattaforme)
        self.harvester_abbattitori = max(0, harvester)
        self.forwarder_caricatori = max(0, forwarder)
        self.kit_motoseghe_professionali = max(0, motoseghe)

    def _allinea_fallback_singoli(self):
        """Sincronizza i valori floats esatti con il dizionario master per non rompere la Dashboard padre."""
        self.serbatoio_ore_grado_A = self.serbatoi_ore["grado_A"]
        self.serbatoio_ore_grado_B = self.serbatoi_ore["grado_B"]
        self.serbatoio_ore_trattori_alta = self.serbatoi_ore["trattori_alta"]
        self.serbatoio_ore_trattori_media = self.serbatoi_ore["trattori_media"]
        self.serbatoio_ore_piattaforme = self.serbatoi_ore["piattaforme"]
        self.serbatoio_ore_harvester = self.serbatoi_ore["harvester"]
        self.serbatoio_ore_forwarder = self.serbatoi_ore["forwarder"]
        self.serbatoio_ore_motoseghe = self.serbatoi_ore["motoseghe"]

    def inizializza_serbatoi_stagionali(self, giorni_utili: int):
        ore_base = giorni_utili * self.ore_giorno_standard

        # Ricarica completa all'inizio di ogni trimestre
        self.serbatoi_ore["grado_A"] = self.operai_grado_A * ore_base
        self.serbatoi_ore["grado_B"] = self.operai_grado_B * ore_base
        self.serbatoi_ore["trattori_alta"] = self.trattori_alta_potenza * ore_base
        self.serbatoi_ore["trattori_media"] = self.trattori_media_potenza * ore_base
        self.serbatoi_ore["piattaforme"] = self.piattaforme_aeree_semoventi * ore_base
        self.serbatoi_ore["harvester"] = self.harvester_abbattitori * ore_base
        self.serbatoi_ore["forwarder"] = self.forwarder_caricatori * ore_base
        self.serbatoi_ore["motoseghe"] = self.kit_motoseghe_professionali * ore_base

        self._allinea_fallback_singoli()

    def calcola_specifiche_richiesta_cantiere(self, tipo_cantiere: str, unita_lavoro: float, indice_attrito: int = 0) -> dict:
        abaco = self.prestazioni_macchine.get(tipo_cantiere)
        if not abaco: return {}

        combi = abaco["squadra"]

        # 1. Determinazione del tetto massimo di linee attivabili in base all'hardware della ditta
        if tipo_cantiere == "impianto": max_mezzi = self.trattori_alta_potenza
        elif tipo_cantiere == "trinciatura": max_mezzi = self.trattori_media_potenza
        elif tipo_cantiere == "potatura": max_mezzi = self.piattaforme_aeree_semoventi
        elif tipo_cantiere == "raccolta_tradizionale": max_mezzi = min(self.trattori_media_potenza, self.kit_motoseghe_professionali)
        elif tipo_cantiere == "raccolta_avanzata": max_mezzi = min(self.harvester_abbattitori, self.forwarder_caricatori)
        else: max_mezzi = 1

        # Interroghiamo direttamente la struttura master centralizzata (self.serbatoi_ore)
        linee_da_operai_A = (self.serbatoi_ore["grado_A"] // self.ore_giorno_standard) // combi["grado_A"] if combi["grado_A"] > 0 else 999
        linee_da_operai_B = (self.serbatoi_ore["grado_B"] // self.ore_giorno_standard) // combi["grado_B"] if combi["grado_B"] > 0 else 999

        linee_attive = max(1, min(max_mezzi, linee_da_operai_A, linee_da_operai_B))

        # 2. Conversione unità biometrica per la raccolta
        if "raccolta" in tipo_cantiere:
            resa_oraria_per_linea = 25.0
            moltiplicatore_attrito = 1.0 + (indice_attrito / 20.0)
            resa_oraria_per_linea = resa_oraria_per_linea / moltiplicatore_attrito
        else:
            resa_oraria_per_linea = abaco["ha_ora_per_linea"] if "ha_ora_per_linea" in abaco else abaco[list(abaco.keys())[0]]

        # 3. Sviluppo orario di linea condiviso
        resa_oraria_collettiva = linee_attive * resa_oraria_per_linea
        ore_linea_nette = unita_lavoro / max(0.001, resa_oraria_collettiva)
        ore_linea_lorde = ore_linea_nette / self.coefficiente_rendimento_cantiere

        ore_trasferta = ore_linea_lorde * 0.15
        ore_lavoro_puro = ore_linea_lorde - ore_trasferta

        # 4. Compilazione della richiesta analitica per risorsa
        richiesta = {}
        for risorsa, quantita in combi.items():
            richiesta[risorsa] = (ore_lavoro_puro + ore_trasferta) * quantita * linee_attive

        richiesta["meta_lavoro_puro"] = ore_lavoro_puro
        richiesta["meta_trasferta"] = ore_trasferta
        richiesta["meta_linee_attive"] = linee_attive
        richiesta["ore_richieste"] = ore_linea_lorde

        return richiesta
        
    def verifica_e_consuma_risorse(self, specifiche_cantiere: dict) -> float:
        """
        Verifica la disponibilità delle risorse per il cantiere.
        Se insufficienti, esegue un lavoro parziale consumando le risorse fino a saturazione.
        Ritorna un float tra 0.0 e 1.0 che indica la percentuale di lavoro completata.
        """
        if not specifiche_cantiere: return 0.0
        
        fattore_completamento = 1.0
        risorsa_critica = None
        
        # 1. Fase di scansione per individuare il collo di bottiglia e calcolare il lavoro parziale
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_") or risorsa == "ore_richieste": continue
        
            serbatoio_corrente = self.serbatoi_ore.get(risorsa, 0.0)
            if ore_richieste > 0 and serbatoio_corrente < ore_richieste:
                # Calcoliamo la percentuale massima che questa risorsa ci permette di fare
                quota_possibile = serbatoio_corrente / ore_richieste
                if quota_possibile < fattore_completamento:
                    fattore_completamento = quota_possibile
                    risorsa_critica = risorsa
        
        # Se il fattore di completamento è 0, la ditta è totalmente ferma su quella risorsa
        if fattore_completamento <= 0.001:
            if risorsa_critica:
                attributo_fallimento = f"fallimenti_{risorsa_critica}"
                if hasattr(self, attributo_fallimento):
                    setattr(self, attributo_fallimento, getattr(self, attributo_fallimento) + 1)
            return 0.0
        
        # 2. Consumo effettivo proporzionato al fattore di completamento (totale o parziale)
        self.ore_lavoro_effettivo += specifiche_cantiere["meta_lavoro_puro"] * fattore_completamento
        self.ore_logistica_trasferta += specifiche_cantiere["meta_trasferta"] * fattore_completamento
        
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_") or risorsa == "ore_richieste": continue
            
            # Detraiamo solo la quota di ore effettivamente spesa nei campi
            ore_effettive_spese = ore_richieste * fattore_completamento
            self.serbatoi_ore[risorsa] = max(0.0, self.serbatoi_ore[risorsa] - ore_effettive_spese)
        
        self._allinea_fallback_singoli()
        
        # Ritorniamo la percentuale di lavoro svolto (1.0 = tutto fatto, < 1.0 = parziale)
        return fattore_completamento

    def calcola_saturazione_macchinario(self, nome_macchinario: str, giorni_utili: int) -> float:
        ore_base = giorni_utili * self.ore_giorno_standard
        
        mappa_nomi = {
            "trattori_alta": "trattori_alta_potenza",
            "trattori_media": "trattori_media_potenza",
            "piattaforme": "piattaforme_aeree_semoventi",
            "harvester": "harvester_abbattitori",
            "forwarder": "forwarder_caricatori",
            "motoseghe": "kit_motoseghe_professionali"
        }
        
        nome_reale_attr = mappa_nomi.get(nome_macchinario, f"num_{nome_macchinario}")
        num_mezzi = getattr(self, nome_reale_attr, 0)
        if num_mezzi == 0: return 0.0

        ore_totali_disponibili = num_mezzi * ore_base
        ore_rimaste_serbatoio = self.serbatoi_ore.get(nome_macchinario, 0.0)
        ore_consumate = ore_totali_disponibili - ore_rimaste_serbatoio

        return round((ore_consumate / ore_totali_disponibili) * 100, 1)