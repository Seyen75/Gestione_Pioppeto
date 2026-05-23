"""
Modulo Core - Rappresentazione ingegneristica avanzata della ditta forestale.
Gestisce l'inventario delle risorse, i serbatoi d'ore stagionali e la diagnostica dei colli di bottiglia.
"""

class Ditta:
    def __init__(self, nome: str = "Azienda Pioppicola Padana"):
        # ANAGRAFICA E PARAMETRI GENERALI
        self.nome_ditta: str = nome
        self.ore_giorno_standard: int = 8
        self.coefficiente_rendimento_cantiere: float = 0.80  # Adeguatamento per Normativa IUFRO (20% tempi accessori) - Da indicare in PW

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

        # SERBATOI ORE STAGIONALI PER SIMULAZIONE
        self.serbatoio_ore_grado_A: float = 0.0
        self.serbatoio_ore_grado_B: float = 0.0
        self.serbatoio_ore_trattori_alta: float = 0.0
        self.serbatoio_ore_trattori_media: float = 0.0
        self.serbatoio_ore_piattaforme: float = 0.0
        self.serbatoio_ore_harvester: float = 0.0
        self.serbatoio_ore_forwarder: float = 0.0
        self.serbatoio_ore_motoseghe: float = 0.0

        # LISTA PRESTAZIONALI UNITARIE. Servirà per la simulazione per avere le basi strutturali per ogni operazione
        self.prestazioni_macchine = {
            "impianto": {
                "ha_ora_per_linea": 0.04,  # 1 Trattore Alta + Equipaggio fa 0.04 ha/h
                "squadra": {"grado_A": 1, "grado_B": 1, "trattori_alta": 1}
            },
            "trinciatura": {
                "ha_ora_per_linea": 0.30,  # 1 Trattore Media fa 0.3 ha/h
                "squadra": {"grado_A": 1, "grado_B": 0, "trattori_media": 1}
            },
            "potatura": {
                "ha_ora_per_linea": 0.08,  # 1 Piattaforma + Equipaggio fa 0.08 ha/h
                "squadra": {"grado_A": 1, "grado_B": 1, "piattaforme": 1}
            },
            "raccolta_tradizionale": {
                "m3_ora_per_linea": 2.5,   # Motoseghe + Verricello (Trattore Media)
                "squadra": {"grado_A": 2, "grado_B": 0, "motoseghe": 1, "trattori_media": 1}
            },
            "raccolta_avanzata": {
                "m3_ora_per_linea": 12.0,  # Linea accoppiata Harvester + Forwarder
                "squadra": {"grado_A": 2, "grado_B": 0, "harvester": 1, "forwarder": 1}
            }
        }

        # REGISTRI DI UTILIZZO E LOGISTICA TOTALI
        self.ore_lavoro_effettivo: float = 0.0
        self.ore_logistica_trasferta: float = 0.0 

        # CONTATORI DI FALLIMENTO (DIAGNOSTICA PER IL REPORT FINALE)
        self.fallimenti_operaio_grado_A: int = 0
        self.fallimenti_operaio_grado_B: int = 0
        self.fallimenti_trattori_alta: int = 0
        self.fallimenti_trattori_media: int = 0
        self.fallimenti_piattaforme_aeree: int = 0
        self.fallimenti_harvester: int = 0
        self.fallimenti_forwarder: int = 0
        self.fallimenti_motoseghe: int = 0

    def configura_risorse(self, op_A: int, op_B: int, t_alta: int, t_media: int,
                          piattaforme: int, harvester: int, forwarder: int, motoseghe: int):
                              
        # Aggiorna l'inventario reale della ditta tramite i dati inseriti nella form
        self.operai_grado_A = max(0, op_A)
        self.operai_grado_B = max(0, op_B)
        self.trattori_alta_potenza = max(0, t_alta)
        self.trattori_media_potenza = max(0, t_media)
        self.piattaforme_aeree_semoventi = max(0, piattaforme)
        self.harvester_abbattitori = max(0, harvester)
        self.forwarder_caricatori = max(0, forwarder)
        self.kit_motoseghe_professionali = max(0, motoseghe)

    def inizializza_serbatoi_stagionali(self, giorni_utili: int):
        # Azzera e ricalcola la capacità oraria disponibile all'inizio di ogni stagione
        ore_base = giorni_utili * self.ore_giorno_standard

        # Reset Uomini
        self.serbatoio_ore_grado_A = self.operai_grado_A * ore_base
        self.serbatoio_ore_grado_B = self.operai_grado_B * ore_base

        # Reset Macchine
        self.serbatoio_ore_trattori_alta = self.trattori_alta_potenza * ore_base
        self.serbatoio_ore_trattori_media = self.trattori_media_potenza * ore_base
        self.serbatoio_ore_piattaforme = self.piattaforme_aeree_semoventi * ore_base
        self.serbatoio_ore_harvester = self.harvester_abbattitori * ore_base
        self.serbatoio_ore_forwarder = self.forwarder_caricatori * ore_base
        self.serbatoio_ore_motoseghe = self.kit_motoseghe_professionali * ore_base

    def calcola_specifiche_richiesta_cantiere(self, tipo_cantiere: str, unita_lavoro: float, indice_attrito: int = 0) -> dict:
        
        # Determina quante ore di linea (e di conseguenza di ogni risorsa) servono per evadere il cantiere.
        # Considera il collo di bottiglia reale della ditta.
        
        abaco = self.prestazioni_macchine.get(tipo_cantiere)
        if not abaco: return {}

        # 1. Calcola linee attivabili contemporaneamente per veificare il collo di bottiglia
        combi = abaco["squadra"]

        # Valutazione di quante squadre potrei comporre guardando i macchinari a disposizione attivabili
        if tipo_cantiere == "impianto": max_mezzi = self.trattori_alta_potenza
        elif tipo_cantiere == "trinciatura": max_mezzi = self.trattori_media_potenza
        elif tipo_cantiere == "potatura": max_mezzi = self.piattaforme_aeree_semoventi
        elif tipo_cantiere == "raccolta_tradizionale": max_mezzi = min(self.trattori_media_potenza, self.kit_motoseghe_professionali)
        elif tipo_cantiere == "raccolta_avanzata": max_mezzi = min(self.harvester_abbattitori, self.forwarder_caricatori)
        else: max_mezzi = 1

        # Valutazione di quante squadre posso effettivamente dotare di equipaggio con gli operai a disposizione
        linee_da_operai_A = (self.serbatoio_ore_grado_A // self.ore_giorno_standard) // combi["grado_A"] if combi["grado_A"] > 0 else 999
        linee_da_operai_B = (self.serbatoio_ore_grado_B // self.ore_giorno_standard) // combi["grado_B"] if combi["grado_B"] > 0 else 999

        # Numero di squadre reali che si muoveranno sul lotto
        linee_attive = max(1, min(max_mezzi, linee_da_operai_A, linee_da_operai_B))

        # Calcolo dei tempi netti e lordi dilatati dall'attrito logistico
        resa_oraria_collettiva = linee_attive * abaco["ha_ora_per_linea"] if "m3_" not in list(abaco.keys())[0] else linee_attive * abaco["m3_ora_per_linea"]

        # Se è un cantiere forestale di taglio, applico il moltiplicatore d'attrito
        if "raccolta" in tipo_cantiere:
            moltiplicatore_attrito = 1.0 + (indice_attrito / 20.0) # Fino a +50% di tempo richiesto
            resa_oraria_collettiva = resa_oraria_collettiva / moltiplicatore_attrito

        ore_linea_nette = unita_lavoro / max(0.001, resa_oraria_collettiva)
        ore_linea_lorde = ore_linea_nette / self.coefficiente_rendimento_cantiere

        # Scorporo la trasferta logistica per il registro (fissa al 15% del tempo lordo)
        ore_trasferta = ore_linea_lorde * 0.15
        ore_lavoro_puro = ore_linea_lorde - ore_trasferta

        # Compilazione della richiesta specifica per risorsa (Moltiplicando ore linea * fabbisogno squadra)
        richiesta = {}
        for risorsa, quantita in combi.items():
            richiesta[risorsa] = (ore_lavoro_puro + ore_trasferta) * quantita

        # Ritorno dei metadati di tracciamento utili alla funzione principale
        richiesta["meta_lavoro_puro"] = ore_lavoro_puro
        richiesta["meta_trasferta"] = ore_trasferta
        richiesta["meta_linee_attive"] = linee_attive

        return richiesta

    def verifica_e_consuma_risorse(self, specifiche_cantiere: dict) -> bool:
        
        # Controlla in parallelo tutti i serbatoi d'ore necessari.
        # Se superato, scala le ore e aggiorna i registri cumulativi. In caso di fallimento incrementa il contatore diagnostico specifico del blocco.
        
        if not specifiche_cantiere: return False

        # Verifica simultanea delle capienze d'ore stagionali
        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_"): continue  # Salta i metadati informativi

            serbatoio_corrente = getattr(self, f"serbatoio_ore_{risorsa}", 0.0)
            if serbatoio_corrente < ore_richieste:
                # Incrementa il contatore fallimento della risorsa satura
                contatore_fallimento = f"fallimenti_{risorsa}"
                if hasattr(self, contatore_fallimento):
                    setattr(self, contatore_fallimento, getattr(self, contatore_fallimento) + 1)
                return False

        # Consumo effettivo e scarico nei registri di contabilità ditta
        self.ore_lavoro_effettivo += specifiche_cantiere["meta_lavoro_puro"]
        self.ore_logistica_trasferta += specifiche_cantiere["meta_trasferta"]

        for risorsa, ore_richieste in specifiche_cantiere.items():
            if risorsa.startswith("meta_"): continue
            nuovo_valore = getattr(self, f"serbatoio_ore_{risorsa}") - ore_richieste
            setattr(self, f"serbatoio_ore_{risorsa}", nuovo_valore)

        return True

    def calcola_saturazione_macchinario(self, nome_macchinario: str, giorni_utili: int) -> float:
        # Restituisce la percentuale di utilizzo reale di una flotta rispetto alla sua capacità stagionale
        
        ore_base = giorni_utili * self.ore_giorno_standard
        num_mezzi = getattr(self, f"num_{nome_macchinario}", 0)
        if num_mezzi == 0: return 0.0

        ore_totali_disponibili = num_mezzi * ore_base
        ore_rimaste_serbatoio = getattr(self, f"serbatoio_ore_{nome_macchinario}", 0.0)
        ore_consumate = ore_totali_disponibili - ore_rimaste_serbatoio

        return round((ore_consumate / ore_totali_disponibili) * 100, 1)