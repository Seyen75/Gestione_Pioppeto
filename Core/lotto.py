
import math, random

class Lotto:
    def __init__(self, id_lotto: str, superficie: float, sesto_impianto: str = "6x6"):
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
        self.metri_potatura_effettivi: float = 0.0
        self.stato_infestanti: float = 0.0
        self.anni_ritardo_taglio: int = 0
        self.tagliato: bool = False
        
        # FLAG E REGISTRI (PW)
        self.immissione_effettuata: bool = False
        self.malus_colturale_accumulato: float = 0.0
        self.cronistoria_lavorazioni_saltate: list = []
        self.archivio_storico_lavorazioni_saltate: list = []
        self.report_resa_finale: dict = {}



    def _calcola_densita(self, sesto: str) -> int:
        """Mappa il sesto di impianto alla densità piante/ha."""
        # Esempio: 6x6=36mq -> 10000/36 = 277 piante/ha
        mappa = {"6x6": 277, "6x5": 333, "5x5": 400, "5x4": 500, "4x4": 625, "7x6": 238, "7x7": 204}
        return mappa.get(sesto, 277)



    def inizializza_nuovo_ciclo(self):
        """Resetta le variabili per un nuovo ciclo di vita del pioppeto."""
                
        # 1. Reset operativo
        self.immissione_effettuata = False 
        self.malus_colturale_accumulato = 0.0
        self.anni_ritardo_taglio = 0
        self.stato_infestanti = 0.0
        self.tagliato = False
        self.cronistoria_lavorazioni_saltate = []
        self.report_resa_finale = {}
        
        # 2. Reset Biometrico Incondizionato (Niente if self.eta == 0)
        self.diametro_medio_fusto = 0.0
        self.altezza_media_piante = 0.0
        self.metri_potatura_effettivi = 0.0
        
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


    # --- PROPERTIES DI ALIAS ---
    @property
    def clone_scelto(self): return self.clone_assegnato
    @clone_scelto.setter
    def clone_scelto(self, value): self.clone_assegnato = value

    @property
    def superficie(self) -> float: return self.superficie_ettari
    @superficie.setter
    def superficie(self, value: float): self.superficie_ettari = value

    def presets_fallback_strutturale(self) -> dict:
        return {
            "parametri_crescita": {"incremento_medio_annuo_ottimale": 25.0, "coefficiente_forma": 0.42},
            "proprieta_tecnologiche": {"densita_verde_t_m3": 0.85},
            "esigenze_trattamenti": {"sensibilita_marsonina": "Media"}
        }



    def registra_fallimento_intervento(self, operazione: str, stagione: str, anno: int):
        record_anomalia = {"anno": anno, "stagione": stagione, "operazione": operazione}
        self.cronistoria_lavorazioni_saltate.append(record_anomalia)
        self.archivio_storico_lavorazioni_saltate.append(record_anomalia)


    def verifica_maturita_raccolta(self) -> bool:
        if self.destinazione_uso == "OPERA":
            eta_minima_verifica = 10
            diametro_target = 30
            limite_massimo_ritardo = 5
        else:
            eta_minima_verifica = 5
            diametro_target = 15.0
            limite_massimo_ritardo = 3

        if self.eta < eta_minima_verifica: return False
        
        if self.diametro_medio_fusto < diametro_target:
            if self.anni_ritardo_taglio >= limite_massimo_ritardo: return True
            return False
        return True

    # Funzione per calcolare sul singolo lotti in fase di taglio le quantità di resa per tipologia che si otterrà
    # La funzione distingue fra lotti da OPERA e INDUSTRIA. I lotti da OPERA daranno porzione di resa anche alla resa per cartiera e truciolato con le percentuali di alberi non idonei
    # I lotti da INDUSTRIA invece non danno mai resa da opera, ma ha una porzione di materiale che va in truciolato
    # La funzione, attraverso la valutazione di una curva guassiana stima, con una porzione piccola randomica per evitare rese eccessiavamente simili, le ripartizioni

    def calcola_ripartizione_assortimenti(self, parametri_clone_selezionato: dict, piante_abbattute: int) -> dict:
        
        # INIZIALIZZAZIONE SICURA DELLE VARIABILI
        resa_opera_m3 = 0.0
        resa_cartiera_ton = 0.0
        resa_truciolato_ton = 0.0
        
        if piante_abbattute <= 0:
            return {"opera_m3": 0.0, "cartiera_t": 0.0, "truciolato_t": 0.0}

        param_crescita = parametri_clone_selezionato.get("parametri_crescita", {})
        param_tecnologici = parametri_clone_selezionato.get("proprieta_tecnologiche", {})
        coeff_forma = param_crescita.get("coefficiente_forma", 0.42)
        densita_verde = param_tecnologici.get("densita_verde_t_m3", 0.85)
        diametro_obiettivo = param_crescita.get("diametro_obiettivo_cm", 30.0)

        d_m = self.diametro_medio_fusto / 100.0
        volume_cantiere_m3 = (d_m ** 2) * self.altezza_media_piante * coeff_forma * piante_abbattute
        
        # Il volume lordo totale influenzato dallo storico vitale del lotto
        volume_cantiere_m3 *= self.moltiplicatore_efficienza_clone

        if self.destinazione_uso == "OPERA":
            if self.diametro_medio_fusto >= diametro_obiettivo:
                # --- CALCOLO STATISTICO CON DISTRIBUZIONE NORMALE ---
                # Moduliamo la media in base all'efficienza vitale del lotto. 
                # Un clone sofferente produrrà meno legno da sfogliato.
                mu_opera = 0.62 * min(1.0, self.moltiplicatore_efficienza_clone) 
                
                # Applichiamo la Gaussiana (Media, Deviazione Standard)
                quota_opera = random.gauss(mu_opera, 0.04) 
                quota_cartiera = random.gauss(0.20, 0.03)
                quota_truciolato = random.gauss(0.18, 0.03)
                
                # Evitiamo valori fuori range (es. negativi in casi estremi)
                quota_opera = max(0.40, min(0.75, quota_opera))
                quota_cartiera = max(0.10, min(0.35, quota_cartiera))
                quota_truciolato = max(0.05, min(0.30, quota_truciolato))
                
                # Normalizzazione: assicuriamoci che la somma faccia sempre 1.0 (100%)
                somma_quote = quota_opera + quota_cartiera + quota_truciolato
                quota_opera /= somma_quote
                quota_cartiera /= somma_quote
                quota_truciolato /= somma_quote

                resa_opera_m3 = volume_cantiere_m3 * quota_opera
                resa_cartiera_ton = (volume_cantiere_m3 * quota_cartiera) * densita_verde
                resa_truciolato_ton = (volume_cantiere_m3 * quota_truciolato) * densita_verde
            else:
                # Taglio anticipato/immaturo (Ritardo strutturale o abbattimento forzato)
                fattore_efficienza = self.diametro_medio_fusto / diametro_obiettivo
                
                # Più il diametro è lontano dall'obiettivo, più la Gaussiana collassa
                mu_opera_ridotta = 0.62 * (fattore_efficienza ** 2.5) 
                quota_opera_reale = max(0.0, random.gauss(mu_opera_ridotta, 0.05))
                
                quota_residua = 1.0 - quota_opera_reale
                
                # Il residuo si divide tra cartiera e truciolato (con leggera varianza)
                var_residuo = random.gauss(0.50, 0.05)
                
                resa_opera_m3 = volume_cantiere_m3 * quota_opera_reale
                resa_cartiera_ton = (volume_cantiere_m3 * (quota_residua * var_residuo)) * densita_verde
                resa_truciolato_ton = (volume_cantiere_m3 * (quota_residua * (1.0 - var_residuo))) * densita_verde
        else:
            # DESTINAZIONE INDUSTRIA
            mu_cartiera = 0.88 * min(1.0, self.moltiplicatore_efficienza_clone)
            quota_cartiera = random.gauss(mu_cartiera, 0.03)
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
            "opera_m3": round(resa_opera_m3, 2),
            "cartiera_t": round(resa_cartiera_ton, 2),
            "truciolato_t": round(resa_truciolato_ton, 2)
        }
    
    # Funzione che valuta l'adattabilità del clone al terreno del lotto, restituendo un moltiplicatore che influenzerà la crescita biologica simulata
  
    def calcola_moltiplicatore_idrico(self) -> float:
        """
        Valuta l'adattabilità (vocazione) del clone al terreno del lotto.
        Valore fisso strutturale tra -1.0 e +1.0.
        
        +1.0 = Scelta perfetta (Es. terreno golenale freschissimo) -> +10% di crescita annua
         0.0 = Terreno standard (Neutro) -> Crescita 100% (1.0)
        -1.0 = Scelta errata (Es. terreno arido o inadatto) -> -15% di crescita annua
        """
        idx = getattr(self, "indice_tendenza_idrica", 0.0)
        
        if idx >= 0:
            # Bonus lineare: fino a un massimo del +10%
            return 1.0 + (0.10 * idx)
        else:
            # Malus lineare morbido: fino a un massimo del -15%
            return 1.0 - (0.15 * abs(idx))

    # Funzione che simula l'accrescimento biologico del lotto per un anno, restituendo i dati aggiornati di diametro, altezza, volume e piante vive

    def simula_accrescimento(self, profilo_clone: dict, eta_anno: int) -> dict:
        if eta_anno == 0:
            return {"dbh_reale_cm": 0.0, "altezza_m": 0.0, "volume_singolo_m3": 0.0, "piante_attive": self.numero_piante_vive, "volume_totale_m3": 0.0}

        param = profilo_clone["parametri_crescita"]
        
        if self.destinazione_uso == "INDUSTRIA":
            A = param["incremento_medio_annuo_ottimale"] * 1.20
            eta_rot = 5
            k = 1.5 / eta_rot  
        else:
            A = param["incremento_medio_annuo_ottimale"] * 1.45
            eta_rot = param["eta_rotazione_standard"]
            k = 2.2 / eta_rot  

        p = 1.02 if profilo_clone["esigenze_trattamenti"].get("frequenza_irrigazione_anni_1_2") == "Alta" else 1.05
        
        # 1. Moltiplicatore ambientale (Vocazione fissa del terreno + Errori colturali accumulati)
        vocazione_terreno = self.calcola_moltiplicatore_idrico()
        mult_reale = max(0.40, vocazione_terreno - getattr(self, "malus_colturale_accumulato", 0.0))

        # 2. CALCOLO ASSOLUTO (Ripristinato: sicuro per l'architettura del tuo motore)
        dbh_teorico = (A * ((1.0 - math.exp(-k * eta_anno)) ** p)) * mult_reale
        
        # Salvaguardia: la pianta mantiene il diametro massimo raggiunto in caso di malus estremi
        dbh_precedente = getattr(self, "diametro_medio_fusto", 0.0)
        dbh = max(dbh_precedente, dbh_teorico)

        # 3. Calcolo Altezza e Volume
        h = (dbh * 0.6) + 4.0 if eta_anno <= 5 else min(27.5, 17.0 + (1.2 * (dbh - 20)))
        vol_singolo = (math.pi * ((dbh / 200) ** 2)) * h * param["coefficiente_forma"]

        # 4. Mortalità
        if eta_anno == 1:
            immissione_fatta = getattr(self, "immissione_effettuata", False)
            tasso = 0.007 if immissione_fatta else 0.07
            piante_vive = int((self.superficie_ettari * self.densita_iniziale) * (1.0 - tasso))
        else:
            tasso = 0.012 if eta_anno <= 5 else (0.018 if eta_anno <= 10 else 0.025)
            piante_vive = int(self.numero_piante_vive * (1.0 - tasso))
        
        return {
            "dbh_reale_cm": round(dbh, 2), 
            "altezza_m": round(h, 2),
            "volume_singolo_m3": round(vol_singolo, 4), 
            "piante_attive": max(0, piante_vive),
            "volume_totale_m3": round(vol_singolo * max(0, piante_vive), 2)
        }