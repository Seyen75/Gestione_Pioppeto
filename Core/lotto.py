
import math, random

class Lotto:
    
    # ATTRIBUTI FISSI E INIZIALI
    
    def __init__(self, id_lotto: str, superficie: float, sesto_impianto: str = "6x6"):
        '''Inizializza un nuovo lotto con i parametri di base. Il sesto di impianto determina la densità iniziale di piante per ettaro.'''
        
        # PARAMETRI IDENTIFICATIVI E FISICI
        self.id_lotto: str = id_lotto
        self.superficie_ettari: float = superficie
        
        # Gestione dinamica del sesto (calcolata in base al sesto scelto)
        self.sesto_impianto: str = sesto_impianto
        self.densita_iniziale: int = self._calcola_densita(sesto_impianto)
        
        # PARAMETRI AMBIENTALI E CLONALI
        self.indice_attrito_spaziale: int = 0   
        self.indice_tendenza_idrica: float = 0.0 
        self.clone_assegnato: str = "I-214"
        self.destinazione_uso: str = "OPERA"
        self.moltiplicatore_efficienza_clone: float = 1.0

        # VARIABILI DI STATO BIOLOGICHE DINAMICHE
        self.eta: int = 0
        self.numero_piante_vive: int = int(self.superficie_ettari * self.densita_iniziale)
        self.diametro_medio_fusto: float = 0.0
        self.altezza_media_piante: float = 0.0
        self.anni_ritardo_taglio: int = 0
        self.tagliato: bool = False
        
        # VARIABILI DI STATO OPERATIVE
        self.immissione_effettuata: bool = False
        self.malus_colturale_accumulato: float = 0.0
        self.report_resa_finale: dict = {}

    # PROPERTIES DI ALIAS
    @property
    def clone_scelto(self): return self.clone_assegnato
    @clone_scelto.setter
    def clone_scelto(self, value): self.clone_assegnato = value

    @property
    def superficie(self) -> float: return self.superficie_ettari
    @superficie.setter
    def superficie(self, value: float): self.superficie_ettari = value

   
    def _calcola_densita(self, sesto: str) -> int:
        '''Restituisce la densità iniziale di piante per ettaro in base al sesto di impianto scelto.'''
        mappa = {"6x6": 277, "6x5": 333, "5x5": 400, "5x4": 500, "4x4": 625, "7x6": 238, "7x7": 204}
        return mappa.get(sesto, 277)


    def inizializza_nuovo_ciclo(self):
        """Resetta le variabili per un nuovo ciclo di vita del pioppeto."""
                
        # 1. Reset operativo
        self.immissione_effettuata = False 
        self.malus_colturale_accumulato = 0.0
        self.anni_ritardo_taglio = 0
        self.tagliato = False
        self.cronistoria_lavorazioni_saltate = []
        self.report_resa_finale = {}
        
        # 2. Reset Biometrico Incondizionato
        self.diametro_medio_fusto = 0.0
        self.altezza_media_piante = 0.0
        
        # 3. Reset piante (calcolo base)
        self.numero_piante_vive = int(self.superficie_ettari * self.densita_iniziale)

        # 4. RESET DELLA CACHE DEL SIMULATORE
        self.dati_correnti = {
            "dbh_reale_cm": 0.0, 
            "altezza_m": 0.0, 
            "volume_singolo_m3": 0.0, 
            "piante_attive": self.numero_piante_vive, 
            "volume_totale_m3": 0.0
        }


    def esegui_raccolta(self, piante_abbattute: int, clone_profilo: dict) -> tuple[dict, str]:
            '''Esegue la raccolta del lotto, calcolando le rese e aggiornando lo stato delle piante. Se il lotto è completamente abbattuto, viene resettato per un nuovo ciclo. 
            Restituisce un dizionario con le rese e una stringa con lo stato dell'esecuzione.'''
            # Calcolo rese
            rese = self.calcola_ripartizione_assortimenti(clone_profilo, piante_abbattute)
            
            # Aggiornamento stato piante
            self.numero_piante_vive = max(0, self.numero_piante_vive - piante_abbattute)
            self.dati_correnti["piante_attive"] = self.numero_piante_vive
            
            # Logica di reset ciclo o aggiornamento stato
            if self.numero_piante_vive <= 5:
                self.inizializza_nuovo_ciclo()
                stato_esecuzione = "Eseguito (Taglio Completato - Reset Ciclo)"
            else:
                self.tagliato = True
                self.anni_ritardo_taglio += 1
                stato_esecuzione = f"Eseguito Parziale (In piedi {self.numero_piante_vive} piante)"
                
            return rese, stato_esecuzione

    
    def applica_lavorazione(self, operazione: str, tipo_cantiere: str, percentuale: float, stagione: str, anno: int, profilo_clone: dict, priorita: int):
        """
        Aggiorna lo stato interno del lotto basandosi sull'esito di una lavorazione.
        Restituisce lo stato dell'esecuzione come stringa.
        """
        # 1. Caso successo
        if percentuale >= 0.99:
            if "impianto" in tipo_cantiere.lower() or "astoni" in operazione.lower():
                self.immissione_effettuata = True
            
            if tipo_cantiere == "impianto" and self.numero_piante_vive == 0:
                self.numero_piante_vive = int(self.superficie_ettari * self.densita_iniziale)
                self.dati_correnti["piante_attive"] = self.numero_piante_vive
            
            return "Eseguito"

        # 2. Caso fallimento/parziale
        stato = f"Eseguito Parziale ({int(percentuale * 100)}%)" if percentuale > 0.001 else "Bloccato"
        self.registra_fallimento_intervento(operazione, stagione, anno)
        
        # Gestione Malus (spostata qui dal motore)
        if percentuale <= 0.001:
            sensibilita = profilo_clone["esigenze_trattamenti"].get("sensibilita_marsonina", "Media")
            self.applica_malus_da_fallimento(operazione, tipo_cantiere, sensibilita, priorita)
            
        return stato
    
    
    def verifica_maturita_raccolta(self) -> bool:
        TOLLERANZA_PERCENTUALE = 0.03 
        
        if self.destinazione_uso == "OPERA":
            eta_minima_verifica = 10
            diametro_target = 35.0 
            limite_massimo_ritardo = 5
        else:
            eta_minima_verifica = 5
            diametro_target = 15.0
            limite_massimo_ritardo = 3

        if self.eta < eta_minima_verifica: 
            return False
        
        soglia_elastica = diametro_target * (1.0 - TOLLERANZA_PERCENTUALE)
        
        if self.diametro_medio_fusto >= soglia_elastica:
            return True
            
        if self.anni_ritardo_taglio >= limite_massimo_ritardo:
            return True
            
        return False


    def calcola_ripartizione_assortimenti(self, parametri_clone_selezionato: dict, piante_abbattute: int) -> dict:
        '''Calcola la ripartizione degli assortimenti (Opera, Cartiera, Truciolato) in base al profilo del clone, alla destinazione d'uso e al numero di piante abbattute. 
        Restituisce un dizionario con le rese per ogni tipologia.'''
        
        # INIZIALIZZAZIONE DELLE VARIABILI
        volume_cantiere_m3 = 0.0
        resa_opera_m3 = 0.0
        resa_cartiera_ton = 0.0
        resa_truciolato_ton = 0.0
        
        if piante_abbattute <= 0:
            return {"volume_cantiere_m3": 0.0, "opera_m3": 0.0, "cartiera_t": 0.0, "truciolato_t": 0.0}

        param_crescita = parametri_clone_selezionato["parametri_crescita"]
        param_tecnologici = parametri_clone_selezionato["proprieta_tecnologiche"]
        coeff_forma = param_crescita["coefficiente_forma"]
        densita_verde = param_tecnologici["densita_verde_t_m3"]
        
        diametro_obiettivo = 35.0 if self.destinazione_uso == "OPERA" else 15.0

        # Calcolo del volume lordo reale (già influenzato dallo storico di crescita)
        d_m = self.diametro_medio_fusto / 100.0
        volume_cantiere_m3 = (d_m ** 2) * self.altezza_media_piante * coeff_forma * piante_abbattute

        if self.destinazione_uso == "OPERA":
            # Calcolo Indice Qualità Legname
            # Un malus di 0.0 significa fusto perfetto (indice 1.0).
            # Un malus alto riduce linearmente la qualità (es. i nodi impediscono di fare l'Opera)
            malus_storico = self.malus_colturale_accumulato
            indice_qualita_fusto = max(0.60, 1.0 - (malus_storico * 0.4)) 
            
            mu_opera = 0.62 * indice_qualita_fusto 
            quota_opera = max(0.01, random.gauss(mu_opera, 0.04))
            quota_cartiera = max(0.01, random.gauss(0.20, 0.03))
            quota_truciolato = max(0.01, random.gauss(0.18, 0.03))

            somma_quote = quota_opera + quota_cartiera + quota_truciolato
            quota_opera /= somma_quote
            quota_cartiera /= somma_quote
            quota_truciolato /= somma_quote

            resa_opera_m3 = volume_cantiere_m3 * quota_opera
            resa_cartiera_ton = (volume_cantiere_m3 * quota_cartiera) * densita_verde
            resa_truciolato_ton = (volume_cantiere_m3 * quota_truciolato) * densita_verde
        else:
            # DESTINAZIONE INDUSTRIA (Biomassa/Cartiera pura)
            quota_cartiera = random.gauss(0.88, 0.03)
            quota_cartiera = max(0.75, min(0.95, quota_cartiera))
            quota_truciolato = 1.0 - quota_cartiera
            resa_cartiera_ton = (volume_cantiere_m3 * quota_cartiera) * densita_verde
            resa_truciolato_ton = (volume_cantiere_m3 * quota_truciolato) * densita_verde

        # Aggiornamento contatori
        self.report_resa_finale.setdefault("opera_m3", 0.0)
        self.report_resa_finale["opera_m3"] += resa_opera_m3
        self.report_resa_finale.setdefault("cartiera_t", 0.0)
        self.report_resa_finale["cartiera_t"] += resa_cartiera_ton
        self.report_resa_finale.setdefault("truciolato_t", 0.0)
        self.report_resa_finale["truciolato_t"] += resa_truciolato_ton

        return {
            "volume_cantiere_m3": round(volume_cantiere_m3, 2),
            "opera_m3": round(resa_opera_m3, 2),
            "cartiera_t": round(resa_cartiera_ton, 2),
            "truciolato_t": round(resa_truciolato_ton, 2)
        }
    
  
    def calcola_moltiplicatore_idrico(self) -> float:
        '''Calcola un moltiplicatore che rappresenta l'adattabilità del clone al terreno del lotto, influenzando la crescita.'''

        idx = getattr(self, "indice_tendenza_idrica", 0.0)
        
        if idx >= 0:
            # Bonus lineare: fino a un massimo del +10%
            return 1.0 + (0.10 * idx)
        else:
            # Malus lineare morbido: fino a un massimo del -15%
            return 1.0 - (0.15 * abs(idx))


    def simula_accrescimento(self, profilo_clone: dict, eta_anno: int) -> dict:
        '''Simula l'accrescimento del lotto per un anno, restituendo un dizionario con i nuovi parametri biometrici e di resa.'''
        if eta_anno == 0:
            return {
                "dbh_reale_cm": 0.0, 
                "altezza_m": 0.0, 
                "volume_singolo_m3": 0.0, 
                "piante_attive": self.numero_piante_vive, 
                "volume_totale_m3": 0.0
            }

        param = profilo_clone["parametri_crescita"]
        
        # La destinazione d'uso influenza la curva di crescita: i lotti da INDUSTRIA, essendo più orientati alla produzione rapida,
        # hanno una crescita iniziale più veloce ma un plateau più basso, mentre quelli da OPERA crescono più lentamente ma raggiungono diametri maggiori.
        if self.destinazione_uso == "INDUSTRIA":
            A = param["incremento_medio_annuo_ottimale"] * 1.20
            eta_rot = 5
            k = 1.5 / eta_rot  
        else:
            A = param["incremento_medio_annuo_ottimale"] * 1.65
            eta_rot = param["eta_rotazione_standard"]
            k = 2.2 / eta_rot  

        p = 1.02 if profilo_clone["esigenze_trattamenti"].get("frequenza_irrigazione_anni_1_2") == "Alta" else 1.05
        
        # Simula l'andamento meteo annuale (un numero casuale gaussiano centrato sullo 0 con deviazione standard del 5%)
        fluttuazione_stagionale = random.gauss(0.0, 0.05) 
        
        # Moltiplicatore ambientale dinamico
        vocazione_terreno = self.calcola_moltiplicatore_idrico()
        
        # Integrazione della fluttuazione stocastica direttamente nel moltiplicatore reale di crescita
        mult_reale = vocazione_terreno - self.malus_colturale_accumulato + fluttuazione_stagionale
        mult_reale = max(0.35, min(1.30, mult_reale)) # Cap di sicurezza per evitare crescite o blocchi assurdi

        # Calcolo del DBH teorico condizionato dall'ambiente stocastico
        dbh_teorico = (A * ((1.0 - math.exp(-k * eta_anno)) ** p)) * mult_reale
        
        # Salvaguardia biologica (il diametro non si restringe se l'anno è pessimo, gli alberi non tornano indietro, ma possono solo crescere o stagnare)
        dbh_precedente = self.diametro_medio_fusto
        dbh = max(dbh_precedente, dbh_teorico)

        # micro-rumore sul coefficiente d'andamento altezza/diametro per evitare curve di crescita troppo regolari
        rumore_allometrico = random.uniform(-0.03, 0.03)
        if eta_anno <= 5:
            h = (dbh * (0.6 + rumore_allometrico)) + 4.0
        else:
            h = min(27.5, (17.0 + rumore_allometrico * 10) + (1.2 * (dbh - 20)))
        
        # Calcolo Volume Singolo
        vol_singolo = (math.pi * ((dbh / 200) ** 2)) * h * param["coefficiente_forma"]

        # --- INTRODUZIONE MORTALITÀ STOCASTICA ---
        # La mortalità in natura non è una quota fissa, risente di eventi locali casuali
        if eta_anno == 1:
            immissione_fatta = self.immissione_effettuata
            tasso_base = 0.007 if immissione_fatta else 0.07
            # Fluttuazione del tasso di mortalità iniziale
            tasso_reale = max(0.002, tasso_base + random.uniform(-0.02, 0.02))
            piante_vive = int((self.superficie_ettari * self.densita_iniziale) * (1.0 - tasso_reale))
        else:
            tasso_base = 0.012 if eta_anno <= 5 else (0.018 if eta_anno <= 10 else 0.025)
            # Aggiungiamo una variazione casuale basata anche sul malus accumulato
            influenza_malus = self.malus_colturale_accumulato * 0.1
            tasso_reale = max(0.005, tasso_base + random.uniform(-0.005, 0.01) + influenza_malus)
            piante_vive = int(self.numero_piante_vive * (1.0 - tasso_reale))
        
        return {
            "dbh_reale_cm": round(dbh, 2), 
            "altezza_m": round(h, 2),
            "volume_singolo_m3": round(vol_singolo, 4), 
            "piante_attive": max(0, piante_vive),
            "volume_totale_m3": round(vol_singolo * max(0, piante_vive), 2)
        }
        
    
    def get_fase_colturale(self) -> str:
        """Determina la fase di crescita in base all'età del lotto."""
        if self.eta == 0:
            return "0"
        elif self.eta == 1:
            return "1"
        elif 2 <= self.eta <= 4:
            return "Fase_Crescita_Giovane"
        else:
            return "Fase_Mantenimento_Tardo"
    
    
    def registra_fallimento_intervento(self, operazione: str, stagione: str, anno: int):
        """Registra un intervento fallito o bloccato, salvando le informazioni in una cronistoria interna del lotto."""
        if not hasattr(self, "cronistoria_lavorazioni_saltate"):
            self.cronistoria_lavorazioni_saltate = []
        
        self.cronistoria_lavorazioni_saltate.append({
            "operazione": operazione,
            "stagione": stagione,
            "anno": anno
        })
    
    
    def applica_malus_da_fallimento(self, operazione: str, tipo_cantiere: str, sensibilita: str, priorita: int):
        """
        Calcola e accumula il malus in base alla sensibilità del clone e alla priorità dell'intervento.
        """
        # Calcolo del moltiplicatore di danno basato sulla sensibilità del clone
        mult_danno = 1.3 if sensibilita == "Alta" else (0.5 if "bassa" in sensibilita.lower() else 1.0)
        
        # Logica dei pesi basata sulla priorità (riprendiamo quella che avevi nel Simulatore)
        if priorita == 2:
            self.malus_colturale_accumulato += (0.08 * mult_danno)
        elif priorita == 3: 
            self.malus_colturale_accumulato += 0.05
        elif priorita == 4: 
            self.malus_colturale_accumulato += 0.03
        
    
        
    