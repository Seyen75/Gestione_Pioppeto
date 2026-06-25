# Core/ditta.py
# Classe che rappresenta la ditta forestale.
# Gestisce l'inventario delle risorse, i serbatoi d'ore stagionali e la diagnostica dei colli di bottiglia.

class Ditta:
    def __init__(self, nome: str = "Azienda Pioppicola Padana"):
        '''Inizializza la ditta con i parametri di base e le risorse disponibili.'''
        
        # ANAGRAFICA E PARAMETRI GENERALI
        self.nome_ditta: str = nome
        self.ore_giorno_standard: int = 8
        self.coefficiente_rendimento_cantiere: float = 0.80  # Adeguamento per Normativa IUFRO (20% tempi accessori) - Da indicate in PW
        self.coefficiente_iufro: float = 0.80      
        self.tolleranza_taglio: float = 0.1        

        # FORZA LAVORO
        self.operai_grado_A: int = 0  # Specializzati (Conduttori macchine complesse,qualificati per potature alte, ecc.)
        self.operai_grado_B: int = 0  # Generici (Manovali a terra, supporto impianti)

        # PARCO MACCHINE E STRUMENTAZIONI
        self.trattori_alta_potenza: int = 0         # >150 CV (Scasso/Impianto)
        self.trattori_media_potenza: int = 0        # 80-110 CV (Interfilari/Trattamenti)
        self.piattaforme_aeree_semoventi: int = 0   # Ragni elevatori per potatura alta
        self.harvester_abbattitori: int = 0         # Abbattitori pioppicoli a testa rotante
        self.forwarder_caricatori: int = 0          # Caricatori forestali pesanti con ralle
        self.cippatrice: int = 0                    # Cippatrice per residui e ramaglie

        # DIZIONARIO CENTRALIZZATO UNICO DEI SERBATOI ORE (Struttura Master)
        self.serbatoi_ore = {
            "grado_A": 0.0,
            "grado_B": 0.0,
            "trattori_alta": 0.0,
            "trattori_media": 0.0,
            "piattaforme": 0.0,
            "harvester": 0.0,
            "forwarder": 0.0,
            "cippatrice": 0.0,
        }
        
        # REGISTRI DI UTILIZZO E LOGISTICA TOTALI
        self.ore_lavoro_effettivo: float = 0.0

        self.limiti_noli_stagionali = {
            "personale_spec": 10,     
            "personale_comune": 40,   
            "trattori_alta": 5,      
            "trattori_media": 10,    
            "piattaforme": 5,         
            "harvester": 2,
            "forwarder" : 2,
            "cippatrice": 2,
        }
        
        # Registro annuale cumulativo delle ore extra prestate (misure statistiche)
        self.registro_extra_anno = {
            "grado_A": 0.0, "grado_B": 0.0, "trattori_alta": 0.0, "trattori_media": 0.0,
            "piattaforme": 0.0, "harvester": 0.0, "forwarder": 0.0, "cippatrice": 0.0
        }

    # ============================================================
    # GESTIONE RISORSE E SERBATOI
    # ============================================================+

    def inizializza_serbatoi_stagionali(self, giorni_utili: int):
        '''Calcola e ricarica i serbatoi d'ore stagionali in base alle risorse disponibili e ai giorni utili della stagione.'''
        ore_base = giorni_utili * self.ore_giorno_standard

        # Ricarica completa all'inizio di ogni trimestre
        self.serbatoi_ore["grado_A"] = self.operai_grado_A * ore_base
        self.serbatoi_ore["grado_B"] = self.operai_grado_B * ore_base
        self.serbatoi_ore["trattori_alta"] = self.trattori_alta_potenza * ore_base
        self.serbatoi_ore["trattori_media"] = self.trattori_media_potenza * ore_base
        self.serbatoi_ore["piattaforme"] = self.piattaforme_aeree_semoventi * ore_base
        self.serbatoi_ore["harvester"] = self.harvester_abbattitori * ore_base
        self.serbatoi_ore["forwarder"] = self.forwarder_caricatori * ore_base
        self.serbatoi_ore["cippatrice"] = self.cippatrice * ore_base
        # Ricarica delle ore del mercato locale (Risorse Esterne)
        if not hasattr(self, "serbatoi_noli_correnti"):
            self.serbatoi_noli_correnti = {}
            
        for chiave_mercato, unita_max in self.limiti_noli_stagionali.items():
            self.serbatoi_noli_correnti[chiave_mercato] = unita_max * ore_base   
             
    # ============================================================
    # LOGICA DI CALCOLO E REPORTISTICA
    # ============================================================
    
    def calcola_specifiche_richiesta_cantiere(self, tipo_cantiere: str, unita_lavoro: float, ore_unitarie: float, 
                                          composizione_squadra: dict, indice_attrito: int = 0) -> dict:
        '''Calcola la richiesta di risorse per un cantiere specifico.'''
        if not composizione_squadra or ore_unitarie <= 0: return {}

        # Calcolo ore nette
        if "raccolta" in tipo_cantiere:
            moltiplicatore_attrito = 1.0 + (indice_attrito / 20.0)
            ore_lavoro_puro = (unita_lavoro * ore_unitarie) * moltiplicatore_attrito
        else:
            ore_lavoro_puro = unita_lavoro * ore_unitarie
            
        # Calcolo ore lorde (totali per il cantiere)
        ore_totali_lorde = ore_lavoro_puro / self.coefficiente_rendimento_cantiere
        
        # Creazione dizionario richieste
        richiesta = {}
        for risorsa, quantita in composizione_squadra.items():
            richiesta[risorsa] = round(ore_totali_lorde * quantita, 2)

        richiesta["meta_lavoro_puro"] = round(ore_lavoro_puro, 2)
        richiesta["ore_richieste"] = round(ore_totali_lorde, 2)

        return richiesta


    def verifica_e_consuma_risorse(self, specifiche_cantiere: dict) -> float:
        """
        Coordina la verifica delle coperture e ordina lo svuotamento dei serbatoi.
        """
        # Analisi
        percentuale_completamento, risorsa_critica = self._calcola_percentuale_completamento(specifiche_cantiere)
        
        # Esecuzione
        self._esegui_consumo_risorse(specifiche_cantiere, percentuale_completamento, risorsa_critica)
        
        # Ritorno per il motore logico
        if percentuale_completamento <= 0.001:
            return 0.0
        return percentuale_completamento


    def genera_report_consumi(self, serbatoi_iniziali: dict, extra_iniziali: dict) -> dict: 
        '''Genera un report dettagliato dei consumi e delle risorse utilizzate durante la stagione, confrontando i serbatoi iniziali con quelli finali e tenendo conto dei noli extra. 
            Ritorna un dizionario strutturato con le informazioni chiave per la reportistica finale.'''
        report = {
            "risorse_umane_interne": {
                "disponibili_iniziali_A": round(serbatoi_iniziali.get("grado_A", 0.0), 2),
                "disponibili_iniziali_B": round(serbatoi_iniziali.get("grado_B", 0.0), 2),
                "consumate_A": round(serbatoi_iniziali.get("grado_A", 0.0) - self.serbatoi_ore.get("grado_A", 0.0), 2),
                "consumate_B": round(serbatoi_iniziali.get("grado_B", 0.0) - self.serbatoi_ore.get("grado_B", 0.0), 2)
            },
            "macchinari_interni_consumati": {
                chiave: round(serbatoi_iniziali.get(chiave, 0.0) - self.serbatoi_ore.get(chiave, 0.0), 2)
                for chiave in ["harvester", "forwarder", "trattori_alta", "trattori_media", "piattaforme", "cippatrice"]
            },
            "ricorso_terzi_e_noli": {
                chiave: round(self.registro_extra_anno.get(chiave, 0.0) - extra_iniziali.get(chiave, 0.0), 2)
                for chiave in ["grado_A", "grado_B", "trattori_alta", "trattori_media", "harvester", "forwarder", "piattaforme", "cippatrice"]
            }
        }
        return report

        
    def _calcola_percentuale_completamento(self, specifiche_cantiere: dict) -> tuple[float, str]:
        '''Calcola la percentuale di completamento del cantiere basandosi sulle risorse richieste e sulla disponibilità nei serbatoi interni ed esterni. 
        Restituisce anche la risorsa più critica in caso di carenza.'''
        if not specifiche_cantiere: 
            return 0.0, ""
        
        percentuale_completamento = 1.0
        risorsa_critica = ""

        # Analisi delle risorse necessarie per ogni voce della specifica di cantiere.
        # Esclude i metadati dal calcolo e confronta le ore richieste con la disponibilità 
        # nei serbatoi interni. In caso di carenza (deficit), valuta la disponibilità 
        # di risorse a noleggio (mercato). Se il totale erogabile (interno + nolo) 
        # risulta inferiore alle ore richieste, calcola la quota di completamento 
        # possibile e aggiorna la risorsa critica che limita l'operatività.
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_") or risorsa == "ore_richieste": continue
        
            ore_richieste = round(float(ore_richieste), 2)
            serbatoio_interno = round(float(self.serbatoi_ore.get(risorsa, 0.0)), 2)
            
            if ore_richieste > serbatoio_interno:
                deficit = round(ore_richieste - serbatoio_interno, 2)
                categoria_mercato = self._ottieni_chiave_elasticita(risorsa)
                ore_nolo_rimaste = round(float(self.serbatoi_noli_correnti.get(categoria_mercato, 0.0)), 2)
                
                if deficit > ore_nolo_rimaste:
                    ore_totali_erogabili = round(serbatoio_interno + ore_nolo_rimaste, 2)
                    quota_possibile = round(ore_totali_erogabili / max(0.001, ore_richieste), 2) 
                    
                    if quota_possibile < percentuale_completamento:
                        percentuale_completamento = quota_possibile
                        risorsa_critica = risorsa

        return percentuale_completamento, risorsa_critica
    
    
    def _esegui_consumo_risorse(self, specifiche_cantiere: dict, percentuale_completamento: float, risorsa_critica: str):
        '''Esegue lo svuotamento dei serbatoi interni ed esterni in base alla percentuale di completamento calcolata, aggiornando i contatori di lavoro effettivo e i registri di nolo extra.'''
        if percentuale_completamento <= 0.001:
            if risorsa_critica:
                attr_f = f"fallimenti_{risorsa_critica}"
                if hasattr(self, attr_f): setattr(self, attr_f, getattr(self, attr_f) + 1)
            return

        # EROGAZIONE Lavoro Puro Effettivo (per statistiche)
        lavoro_puro_effettivo = round(specifiche_cantiere.get("meta_lavoro_puro", 0.0) * percentuale_completamento, 2)
        self.ore_lavoro_effettivo = round(self.ore_lavoro_effettivo + lavoro_puro_effettivo, 2)
        
        # Svuotamento serbatoi
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_") or risorsa == "ore_richieste": continue
            
            # calcola le ore effettive (con l'eventuale percentuale di completamento dell'operazione)
            ore_richieste = round(float(ore_richieste), 2)
            ore_effettive_spese = round(ore_richieste * percentuale_completamento, 2)
            serbatoio_interno = round(float(self.serbatoi_ore[risorsa]), 2)
            
            # Verifica che le ore necessarie siano presenti nel serbatoio delle ore della ditta, altrimenti passa alla quota dei noli
            if ore_effettive_spese <= serbatoio_interno:
                self.serbatoi_ore[risorsa] = round(serbatoio_interno - ore_effettive_spese, 2)
            else:
                # Verifica quante ore non sono state attivabili con il serbatoio delle ore interne
                quota_esterna = round(ore_effettive_spese - serbatoio_interno, 2)
                self.serbatoi_ore[risorsa] = 0.0
                
                # prende il serbatoio noli e sottrae il valore residuo mettendo un controllo per evitare che i serbatoi possano andare anche di poco a numeri negativi
                categoria_mercato = self._ottieni_chiave_elasticita(risorsa)
                residuo_nolo = round(float(self.serbatoi_noli_correnti.get(categoria_mercato, 0.0)), 2)
                self.serbatoi_noli_correnti[categoria_mercato] = round(max(0.0, residuo_nolo - quota_esterna), 2)
                self.registro_extra_anno[risorsa] = round(self.registro_extra_anno.get(risorsa, 0.0) + quota_esterna, 2)

        # Segnalazione esecuzione parziale
        if percentuale_completamento < 0.99 and risorsa_critica:
            attr_f = f"fallimenti_{risorsa_critica}"
            if hasattr(self, attr_f): setattr(self, attr_f, getattr(self, attr_f) + 1)

    
    def _ottieni_chiave_elasticita(self, nome_risorsa: str) -> str:
        '''Restituisce la chiave di mercato corrispondente per una data risorsa, necessaria per accedere ai serbatoi dei noli.'''
        if nome_risorsa == "grado_A": return "personale_spec"
        elif nome_risorsa == "grado_B": return "personale_comune"
        # Per i mezzi, il nome della risorsa coincide esattamente con la chiave di nolo
        else: return nome_risorsa