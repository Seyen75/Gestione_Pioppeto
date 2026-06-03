# Core/ditta.py
# Modulo Rappresentazione della ditta forestale.
# Gestisce l'inventario delle risorse, i serbatoi d'ore stagionali e la diagnostica dei colli di bottiglia.

class Ditta:
    def __init__(self, nome: str = "Azienda Pioppicola Padana"):
        # ANAGRAFICA E PARAMETRI GENERALI
        self.nome_ditta: str = nome
        self.ore_giorno_standard: int = 8
        self.coefficiente_rendimento_cantiere: float = 0.80  # Adeguamento per Normativa IUFRO (20% tempi accessori) - Da indicate in PW
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
        self.kit_motoseghe_professionali: int = 0   # Per cantiere abbattimento tradicional

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

        # === DIZIONARIO ELASTICITÀ DI MERCATO DISACCOPPIATO (Requisito PW Avanzato) ===
        # Taratura aggiornata per evitare l'inefficacia dei limiti frazionari (1.5) su singole unità.
        # Garantisce il raddoppio minimo (2.0) sia per la manodopera d'alto fusto che per l'Harvester.
        self.moltiplicatori_elasticita = {
            "personale_spec": 2.0,     # Sblocca il raddoppio orario della squadra di Grado A
            "personale_comune": 3.0,   # Ampio ricorso ad avventizi stagionali (+200% ore extra)
            "mezzi_base": 2.5,         # Nolo flessibile di trattori e piattaforme aggiuntive
            "mezzi_spec": 2.0          # Permette l'ingaggio di una seconda linea di taglio completa
        }
        
        # Registro annuale cumulativo delle ore extra prestate (misure statistiche)
        self.registro_extra_anno = {
            "grado_A": 0.0, "grado_B": 0.0, "trattori_alta": 0.0, "trattori_media": 0.0,
            "piattaforme": 0.0, "harvester": 0.0, "forwarder": 0.0, "motoseghe": 0.0
        }

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

    def calcola_specifiche_richiesta_cantiere(self, tipo_cantiere: str, unita_lavoro: float, ore_unitarie: float, composizione_squadra: dict, indice_attrito: int = 0) -> dict:
        if not composizione_squadra or ore_unitarie <= 0: return {}

        linee_possibili = []
        for risorsa, quantita_richiesta in composizione_squadra.items():
            if quantita_richiesta > 0:
                mappa_mezzi = {
                    "trattori_alta": getattr(self, "trattori_alta_potenza", 0),
                    "trattori_media": getattr(self, "trattori_media_potenza", 0),
                    "piattaforme": getattr(self, "piattaforme_aeree_semoventi", 0),
                    "harvester": getattr(self, "harvester_abbattitori", 0),
                    "forwarder": getattr(self, "forwarder_caricatori", 0),
                    "motoseghe": getattr(self, "kit_motoseghe_professionali", 0),
                    "grado_A": getattr(self, "operai_grado_A", 0),
                    "grado_B": getattr(self, "operai_grado_B", 0)
                }
                disponibilita_fisica = mappa_mezzi.get(risorsa, 999)
                linee_possibili.append(disponibilita_fisica // int(quantita_richiesta))

        linee_attive = max(1, min(linee_possibili) if linee_possibili else 1)

        if "raccolta" in tipo_cantiere:
            moltiplicatore_attrito = 1.0 + (indice_attrito / 20.0)
            ore_lavoro_puro = (unita_lavoro * ore_unitarie) * moltiplicatore_attrito
        else:
            ore_lavoro_puro = unita_lavoro * ore_unitarie
            
        ore_totali_lorde = ore_lavoro_puro / self.coefficiente_rendimento_cantiere
        
        richiesta = {}
        for risorsa, quantita in composizione_squadra.items():
            richiesta[risorsa] = ore_totali_lorde * quantita

        richiesta["meta_lavoro_puro"] = ore_lavoro_puro
        richiesta["meta_linee_attive"] = linee_attive
        richiesta["ore_richieste"] = ore_totali_lorde / linee_attive

        return richiesta

    def _ottieni_chiave_elasticita(self, nome_risorsa: str) -> str:
        """Assegna ad ogni singola voce oraria la corretta categoria di elasticità sul mercato padano."""
        if nome_risorsa == "grado_A":
            return "personale_spec"
        elif nome_risorsa == "grado_B":
            return "personale_comune"
        elif nome_risorsa in ["trattori_alta", "trattori_media", "piattaforme"]:
            return "mezzi_base"
        else:
            return "mezzi_spec"  # Harvester, Forwarder e Motoseghe professionali

    def verifica_e_consuma_risorse(self, specifiche_cantiere: dict) -> float:
        """
        Verifica la disponibilità delle risorse fisiche. Se insufficienti, attiva la logica
        degli stagionali e dei noli differenziati per categoria fino al tetto imposto.
        """
        if not specifiche_cantiere: return 0.0
        
        giorni_utili_stagione = 55
        ore_base_stagione = giorni_utili_stagione * self.ore_giorno_standard
        
        fattore_completamento = 1.0
        risorsa_critica = None

        # 1. SCANSIONE CON FILTRI DI ELASTICITÀ ASIMMETRICI
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_") or risorsa == "ore_richieste": continue
        
            serbatoio_corrente = self.serbatoi_ore.get(risorsa, 0.0)
            
            if ore_richieste > serbatoio_corrente:
                deficit = ore_richieste - serbatoio_corrente
                
                # Identifichiamo il moltiplicatore disaccoppiato corretto per questa risorsa
                categoria_mercato = self._ottieni_chiave_elasticita(risorsa)
                moltiplicatore_attivo = self.moltiplicatori_elasticita.get(categoria_mercato, 2.0)
                
                mappa_attributi = {
                    "grado_A": "operai_grado_A", "grado_B": "operai_grado_B",
                    "trattori_alta": "trattori_alta_potenza", "trattori_media": "trattori_media_potenza",
                    "piattaforme": "piattaforme_aeree_semoventi", "harvester": "harvester_abbattitori",
                    "forwarder": "forwarder_caricatori", "motoseghe": "kit_motoseghe_professionali"
                }
                nome_attr = mappa_attributi.get(risorsa)
                quantita_fissa = getattr(self, nome_attr, 0) if nome_attr else 1
                
                # Calcolo del tetto specifico differenziato per questa risorsa
                ore_massime_mercato = quantita_fissa * ore_base_stagione * (moltiplicatore_attivo - 1.0)
                
                if deficit > ore_massime_mercato:
                    # Superato il tetto specifico della categoria
                    ore_totali_erogabili_con_extra = serbatoio_corrente + ore_massime_mercato
                    quota_possibile = ore_totali_erogabili_con_extra / ore_richieste
                    
                    if quota_possibile < fattore_completamento:
                        fattore_completamento = quota_possibile
                        risorsa_critica = risorsa

        if fattore_completamento <= 0.001:
            if risorsa_critica:
                attr_f = f"fallimenti_{risorsa_critica}"
                if hasattr(self, attr_f): setattr(self, attr_f, getattr(self, attr_f) + 1)
            return 0.0

        # 2. CONSUMO E AGGIORNAMENTO REGISTRO EXTRA STATISTICO
        self.ore_lavoro_effettivo += specifiche_cantiere["meta_lavoro_puro"] * fattore_completamento
        
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_") or risorsa == "ore_richieste": continue
            
            ore_effettive_spese = ore_richieste * fattore_completamento
            serbatoio_corrente = self.serbatoi_ore[risorsa]
            
            if ore_effettive_spese <= serbatoio_corrente:
                self.serbatoi_ore[risorsa] = max(0.0, serbatoio_corrente - ore_effettive_spese)
            else:
                quota_externa = ore_effettive_spese - serbatoio_corrente
                self.serbatoi_ore[risorsa] = 0.0
                self.registro_extra_anno[risorsa] += quota_externa

        self._allinea_fallback_singoli()
        
        if fattore_completamento < 0.99 and risorsa_critica:
            attr_f = f"fallimenti_{risorsa_critica}"
            if hasattr(self, attr_f): setattr(self, attr_f, getattr(self, attr_f) + 1)

        return fattore_completamento

    def calcola_saturazione_macchinario(self, nome_macchinario: str, giorni_utili: int) -> float:
        ore_base = giorni_utili * self.ore_giorno_standard
        mappa_nomi = {
            "trattori_alta": "trattori_alta_potenza", "trattori_media": "trattori_media_potenza",
            "piattaforme": "piattaforme_aeree_semoventi", "harvester": "harvester_abbattitori",
            "forwarder": "forwarder_caricatori", "motoseghe": "kit_motoseghe_professionali"
        }
        nome_reale_attr = mappa_nomi.get(nome_macchinario, f"num_{nome_macchinario}")
        num_mezzi = getattr(self, nome_reale_attr, 0)
        if num_mezzi == 0: return 0.0
        ore_totali_disponibili = num_mezzi * ore_base
        ore_rimaste_serbatoio = self.serbatoi_ore.get(nome_macchinario, 0.0)
        return round(((ore_totali_disponibili - ore_rimaste_serbatoio) / ore_totali_disponibili) * 100, 1)