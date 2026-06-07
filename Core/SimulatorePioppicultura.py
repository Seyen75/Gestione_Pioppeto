import os
import json

from typing import Dict, List, Any
from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI

class SimulatorePioppicoltura:
    def __init__(self, ditta: Any, parametri: Any):
        self.ditta = ditta
        self.parametri = parametri  
        self.dati_cloni: Dict[str, Any] = {}
        
        self.stats_globali = {
            "tagli_strutturali_saltati": 0,
            "tagli_biologici_saltati": 0,
            "lavorazioni_generiche_saltate": 0
        }
                
        self._carica_configurazione_cloni()

    
    # Carica dal file cloni.json la configurazione con i dati del cloni standard
    def _carica_configurazione_cloni(self):
        percorso_json = os.path.join(os.path.dirname(__file__), "cloni.json")
        with open(percorso_json, "r", encoding="utf-8") as f:
            self.dati_cloni = json.load(f)

    # Funzione che data l'età del lotto in anni restituisce la chiave della fase di crescita corrispondente per caricare le operazioni specifiche per quella fase 
    # altrimenti restituisce None per caricare quelle generiche per la stagione
    def _get_chiave_fase(self, eta_anno: int) -> str:
        if eta_anno == 0:
            return 0
        elif eta_anno == 1:
            return 1
        elif 2 <= eta_anno <= 4:  # La fase giovane si ferma a 4 anni per liberare la cartiera a 5
            return "Fase_Crescita_Giovane"
        else:
            return "Fase_Mantenimento_Tardo"

    # Funzione che crea la lista degli interventi che sono previsti per la stagione che è in corso di simulazione
    def prevedi_domanda_stagionale(self, is_esecuzione: bool = False) -> List[Dict[str, Any]]:
        
        # Prende i dati della stagione corrente dai parametri globali
        stagione = self.parametri.stagione_corrente
        # Inizializza la lista degli interventi che sarà restituita
        interventi = []
        
        # Cicla su tutti i lotti presenti all'interno della collezione di lotti presenti nella ditta da simulare
        
        for lotto in self.parametri.collezione_lotti:
            # Se i dati correnti del lotto non sono stati ancora calcolati o caricati vengono creati
            if not hasattr(lotto, "dati_correnti") or not lotto.dati_correnti:
                profilo = self.dati_cloni[lotto.clone_assegnato]
                lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
            
            # Se siamo nella fase di pianificazione invernale, verifichiamo che il lotto sia maturo per il taglio
            # per evitare che i dati originali del lotto non siano modificati durante la simulazione di accrescimento
            # che diranno se potremmo tagliare si salvano i dati originali e finita la verifica si reimpostano
            eta_originale = lotto.eta
            diametro_originale = getattr(lotto, "diametro_medio_fusto", 0.0)
            
            # controllo per verificare se siamo all'avvio del software, in tal caso dobbiamo simulare l'accrescimento
            # dei lotti standard fino alla loro età prevista per avere i dati dinamici aggiornati per valutare se è il lotto standard è pronto per il taglio in inverno
            if stagione == "Inverno" and not is_esecuzione:
                if (lotto.eta == 0 and lotto.numero_piante_vive > 0) or lotto.numero_piante_vive > 5:
                    eta_futura = lotto.eta + 1
                    profilo = self.dati_cloni[lotto.clone_assegnato]
                    dati_futuri = lotto.simula_accrescimento(profilo, eta_futura)
                    
                    lotto.eta = eta_futura
                    lotto.diametro_medio_fusto = dati_futuri.get("dbh_reale_cm", 0.0)

            # Verifica se il lotto è pronto per la raccolta
            is_maturo = lotto.verifica_maturita_raccolta()
            
            # Ripristino immediato dello stato originale per non corrompere la simulazione
            lotto.eta = eta_originale
            lotto.diametro_medio_fusto = diametro_originale

            
            # inserisce nella variabile filiera la lista di lavorazioni previste per la tipologia di destinazione d'uso, OPERA o INDUSTRIA 
            filiera = STRUTTURA_LAVORAZIONI[lotto.destinazione_uso]
            
            # Controllo che verifica lo stato del lotto. Se è maturo e non è stato tagliato allora mette fra le operazioni
            # da fare presenti nella lista. Se è inverno non deve fare alcuna operazione perchè ci sarà raccolta
            if is_maturo or getattr(lotto, "tagliato", False):
                ops = filiera["Raccolta"][stagione] if stagione == "Inverno" else []
                is_raccolta = (stagione == "Inverno")
            # se non è maturo o tagliato allora carica fra le operazioni quelle che trova nella lista operazioni
            else:
                # Verifica che tipo di stato di maturazione si trova il lotto per caricare le operazioni specifiche per quella fase di crescita, altrimenti carica quelle generiche per la stagione
                chiave_fase = self._get_chiave_fase(lotto.eta)
                ops = filiera.get(chiave_fase, {}).get(stagione, []) if chiave_fase is not None else []
                is_raccolta = False
            
            
            # Trasforma la lista di operazioni teoriche ops in un preventivo tecnico dettagliato (interventi), calcolando quanto lavoro serve, con quali macchine e per quale superficie.
            for op in ops:
                id_univoco = op.get("id_operazione", "OP_GEN")
                # carica nella variabile la descrizione della operazione id_operazione e della macrocategoria utile per i passi successivi
                if "descrizione" not in op or not op.get("macrocategoria"):
                    id_op = op.get("id_operazione", "ID_SCONOSCIUTO")
                    raise ValueError(f"Configurazione errata per l'operazione '{id_op}': 'descrizione' e 'macrocategoria' sono obbligatorie.")
                
                descrizione_ui = op["descrizione"]
                macrocategoria = op["macrocategoria"]
                
                # Valutazione disponibilità totale (Proprietà + Nolo) per la lavorazione di raccolta sugli harvester.
                # Nel caso non ci fossero harvester la raccolta passerebbe da quella meccanica a quella tradizionale con motosega
                if is_raccolta: 
                    harvester_noleggiabili = getattr(self.ditta, "limiti_noli_stagionali", {}).get("harvester", 0)
                    harvester_totali_disponibili = self.ditta.harvester_abbattitori + harvester_noleggiabili
                    macrocategoria = "raccolta_avanzata" if harvester_totali_disponibili > 0 else "raccolta_tradizionale"
                
                # Calcolo proporzionale superficie per raccolta nel caso si stia per fare una raccolto o altra operazione
                # Nel caso della raccolta rapporta il lavoro rispetto al numero di piante realmente presenti e non alla mera estensione del lotto
                # Se il lotto ha subito una moria grossa di piante il lavoro sarà più breve
                if is_raccolta:
                    piante_teoriche_max = lotto.superficie_ettari * lotto.densita_iniziale
                    rapporto_sopravvivenza = lotto.dati_correnti.get("piante_attive", 0) / max(1, piante_teoriche_max)
                    unita = lotto.superficie_ettari * rapporto_sopravvivenza
                else:
                    unita = lotto.superficie_ettari
                
                # carica dall'operazione quante ore per ettaro servono per la specifica operazione e quante persone\strumentazioni servono
                ore_unitarie = op["ore_ha"]
                squadra = op["risorse"]
                
                # avvia la funzione che calcola le specifiche del cantiere per le specifiche
                # fornisce oltre i dati ottenuti prima anche l'indice di attrito spaziale del lotto, che indica le difficoltà tecniche del lotto
                # per la sua morfologia (pendenza del terreno, vicinanza alla strada, accessibilità, etc)
                spec = self.ditta.calcola_specifiche_richiesta_cantiere(
                    tipo_cantiere = macrocategoria, 
                    unita_lavoro = unita, 
                    ore_unitarie = ore_unitarie,
                    composizione_squadra = squadra,
                    indice_attrito = lotto.indice_attrito_spaziale
                )
                
                # Aggiunge il dizionario dell'intervento creato nella lista degli interventi della stagione
                if spec:
                    interventi.append({
                        "lotto": lotto, 
                        "id_operazione": id_univoco,
                        "operazione": descrizione_ui,
                        "priorita": op.get("priorita", 4), 
                        "tipo_cantiere_chiave": macrocategoria, 
                        "specifiche_richiesta": spec, 
                        "is_raccolta": is_raccolta
                    })
        
        # Conclusa la creazione della lista, prima di essere ritornata alla funzione chiamante, viene ordinata 
        # in base alla chiave priorità, poichè dopo saranno lavorati preventivamente i lotto a priorità più alta
        return sorted(interventi, key=lambda x: x["priorita"])

    # Funzione che esegue le lavorazioni necessarie per la stagione da simulare.
    # Ottiene le lista delle lavorazioni e crea un dizionario di risposta con il report stagionale delle attività svolte
    # che sarà utilizzato per la reportistica di fine simulazione
    
    def esegui_fase_lavorazioni_stagionali(self) -> Dict[str, Any]:
        """Metodo principale che orchestra le lavorazioni della singola stagione."""
        
        # 1. Inizializzazione serbatoi
        stagione_attiva = self.parametri.stagione_corrente
        giorni_utili_stagione = 55 
        self.ditta.inizializza_serbatoi_stagionali(giorni_utili_stagione)
        
        # Snapshot di inizio stagione per calcolo consumi a fine ciclo
        serbatoi_iniziali = self.ditta.serbatoi_ore.copy()
        extra_iniziali = self.ditta.registro_extra_anno.copy()
        
        # Inizializza il report
        report_stagionale = {
            "dettaglio_operazioni": [], 
            "tagli_effettuati": []
        }
    
        lista_interventi_richiesti = self.prevedi_domanda_stagionale(is_esecuzione=True)
    
        # 2. Ciclo di elaborazione degli interventi
        for intervento in lista_interventi_richiesti:
            lotto_target = intervento["lotto"]
            spec = intervento["specifiche_richiesta"]
            
            # Assicurati che i dati di accrescimento siano aggiornati
            self._assicura_dati_lotto_aggiornati(lotto_target)
    
            # Consumo delle risorse
            percentuale_completamento = self.ditta.verifica_e_consuma_risorse(spec)
    
            # Smistamento logico (Raccolta vs Altre operazioni)
            if not intervento["is_raccolta"]:
                self._gestisci_lavorazione_non_raccolta(
                    intervento, lotto_target, spec, percentuale_completamento, report_stagionale, stagione_attiva
                )
            else:
                self._gestisci_raccolta(
                    intervento, lotto_target, spec, percentuale_completamento, report_stagionale
                )
    
        # 3. Finalizzazione report dei consumi aziendali
        return self._finalizza_report_risorse(report_stagionale, serbatoi_iniziali, extra_iniziali)

    # Funzione che data un intervento e il lotto su cui deve essere eseguito, verifica che i dati di accrescimento del lotto siano aggiornati e se non lo sono li calcola

    def _assicura_dati_lotto_aggiornati(self, lotto_target):
        """Verifica ed eventualmente calcola l'accrescimento biologico del lotto."""
        if not hasattr(lotto_target, "dati_correnti") or not lotto_target.dati_correnti:
            if lotto_target.clone_assegnato not in self.dati_cloni:
                raise ValueError(f"Inconsistenza: Il clone {lotto_target.clone_assegnato} non esiste in self.dati_cloni per il lotto {lotto_target.id_lotto}")
            
            profilo = self.dati_cloni[lotto_target.clone_assegnato]
            lotto_target.dati_correnti = lotto_target.simula_accrescimento(profilo, lotto_target.eta)

    # Funzione che gestisce le lavorazioni che non sono raccolta, valutando se sono state eseguite completamente, parzialmente o bloccate
    # aggiornando di conseguenza lo stato del lotto e il report stagionale

    def _gestisci_lavorazione_non_raccolta(self, intervento, lotto_target, spec, percentuale_completamento, report_stagionale, stagione_attiva):
        """Gestisce le lavorazioni generiche (impianto, sarchiatura, ecc.)."""
        tipo_cantiere_chiave = intervento["tipo_cantiere_chiave"]
        
        # Lavoro eseguito al 100%
        if percentuale_completamento >= 0.99:
            stato_esecuzione = "Eseguito"
            if "impianto" in tipo_cantiere_chiave or "astoni" in intervento["operazione"].lower():
                lotto_target.immissione_effettuata = True
            
            if tipo_cantiere_chiave == "impianto" and lotto_target.numero_piante_vive == 0:
                lotto_target.numero_piante_vive = int(lotto_target.superficie_ettari * lotto_target.densita_iniziale)
                lotto_target.dati_correnti["piante_attive"] = lotto_target.numero_piante_vive
        
        # Eseguito Parzialmente
        elif percentuale_completamento > 0.001:
            self.stats_globali["lavorazioni_generiche_saltate"] += 1
            stato_esecuzione = f"Eseguito Parziale ({int(percentuale_completamento * 100)}%)"
            lotto_target.registra_fallimento_intervento(intervento["operazione"], stagione_attiva, self.parametri.anno_corrente)
        
        # Completamente Bloccato
        else:
            self.stats_globali["lavorazioni_generiche_saltate"] += 1
            stato_esecuzione = "Bloccato (Risorse Insufficienti)"
            lotto_target.registra_fallimento_intervento(intervento["operazione"], stagione_attiva, self.parametri.anno_corrente)
            
            sensibilita = self.dati_cloni[lotto_target.clone_assegnato]["esigenze_trattamenti"]["sensibilita_marsonina"]
            if intervento["priorita"] == 2:
                mult_danno = 1.3 if sensibilita == "Alta" else (0.5 if "bassa" in sensibilita.lower() else 1.0)
                lotto_target.malus_colturale_accumulato += (0.08 * mult_danno)
            elif intervento["priorita"] == 3: 
                lotto_target.malus_colturale_accumulato += 0.05
            elif intervento["priorita"] == 4: 
                lotto_target.malus_colturale_accumulato += 0.03

        # ---> LA CORREZIONE È QUI <---
        ore_teoriche = spec.get("meta_lavoro_puro", 0.0) / self.ditta.coefficiente_rendimento_cantiere
        ore_effettive = ore_teoriche * percentuale_completamento

        report_stagionale["dettaglio_operazioni"].append({
            "lotto_id": lotto_target.id_lotto, 
            "id_operazione": intervento["id_operazione"],
            "priorita": intervento["priorita"], 
            "durata_cantiere_h": round(spec["ore_richieste"], 2),
            "ore_lavoro_totali": round(ore_effettive, 2),
            "percentuale_completamento": round(percentuale_completamento * 100, 2),
            "squadre_attive": spec.get("meta_linee_attive", 1),
            "stato": stato_esecuzione
        })
    # Funzione che gestisce le lavorazioni di raccolta, valutando se sono state eseguite completamente, parzialmente o bloccate

    def _gestisci_raccolta(self, intervento, lotto_target, spec, percentuale_completamento, report_stagionale):
        """Gestisce in via esclusiva l'abbattimento (taglio raso) e le sue rese."""
        piante_totali = lotto_target.dati_correnti["piante_attive"]
        p_abbattute = int(piante_totali * percentuale_completamento) if percentuale_completamento < 0.98 else piante_totali
        
        # Calcolo delle rese sulle piante effettivamente abbattute
        if p_abbattute > 0:
            rese = lotto_target.calcola_ripartizione_assortimenti(self.dati_cloni[lotto_target.clone_assegnato], p_abbattute)
            self.parametri.totale_prodotto_opera_m3 += rese["opera_m3"]
            self.parametri.totale_prodotto_cartiera_t += rese["cartiera_t"]
            self.parametri.totale_prodotto_truciolato_t += rese["truciolato_t"]
    
            lotto_target.numero_piante_vive = max(0, lotto_target.numero_piante_vive - p_abbattute)
            lotto_target.dati_correnti["piante_attive"] = lotto_target.numero_piante_vive
            
            report_stagionale["tagli_effettuati"].append({
                "lotto_id": lotto_target.id_lotto, 
                "volume_raccolto_m3": round(lotto_target.dati_correnti.get("volume_singolo_m3", 0.0) * p_abbattute, 2), 
                "rese": rese
            })

        # Valutazione stato finale del lotto post-taglio
        if lotto_target.numero_piante_vive <= 5 or p_abbattute >= piante_totali:
            lotto_target.inizializza_nuovo_ciclo()
            lotto_target.numero_piante_vive = 0 
            lotto_target.tagliato = False
            lotto_target.eta = 0 
            
            lotto_target.anni_ritardo_taglio = 0
            lotto_target.malus_colturale_accumulato = 0.0
            if hasattr(lotto_target, "cronistoria_lavorazioni_saltate"):
                lotto_target.cronistoria_lavorazioni_saltate.clear()
            if hasattr(lotto_target, "archivio_storico_lavorazioni_saltate"):
                lotto_target.archivio_storico_lavorazioni_saltate.clear()
            
            lotto_target.dati_correnti = {
                "dbh_reale_cm": 0.0, "altezza_m": 0.0, 
                "volume_singolo_m3": 0.0, "piante_attive": 0, "volume_totale_m3": 0.0
            }
            stato_esecuzione = "Eseguito (Taglio Completato - Reset Ciclo)"
        else:
            self.stats_globali["tagli_strutturali_saltati"] += 1
            if p_abbattute > 0: lotto_target.tagliato = True
            lotto_target.anni_ritardo_taglio += 1
            
            if p_abbattute == 0:
                stato_esecuzione = "Bloccato (Risorse Insufficienti)"
            else:
                stato_esecuzione = f"Eseguito Parziale (In piedi {lotto_target.numero_piante_vive} piante)"


        # Calcoliamo le ore teoriche E le moltiplichiamo per quanto lavoro è stato effettivamente svolto
        ore_teoriche = spec.get("meta_lavoro_puro", 0.0) / self.ditta.coefficiente_rendimento_cantiere
        ore_effettive = ore_teoriche * percentuale_completamento

        report_stagionale["dettaglio_operazioni"].append({
            "lotto_id": lotto_target.id_lotto, 
            "id_operazione": intervento["id_operazione"], 
            "durata_cantiere_h": round(spec.get("ore_richieste", 0.0), 2), # FABBISOGNO TEORICO
            "ore_lavoro_totali": round(ore_effettive, 2),                  # ORE LAVORATE REALI
            "percentuale_completamento": round(percentuale_completamento * 100, 2),
            "squadre_attive": spec.get("meta_linee_attive", 1),
            "stato": stato_esecuzione
        })

    # Funzione che calcola la differenza tra ore iniziali e finali per stilare il report dei consumi.

    def _finalizza_report_risorse(self, report_stagionale, serbatoi_iniziali, extra_iniziali):
        """Calcola la differenza tra ore iniziali e finali per stilare il report dei consumi."""
        report_stagionale["risorse_umane_interne"] = {
            "disponibili_iniziali_A": round(serbatoi_iniziali.get("grado_A", 0.0), 2),
            "disponibili_iniziali_B": round(serbatoi_iniziali.get("grado_B", 0.0), 2),
            "consumate_A": round(serbatoi_iniziali.get("grado_A", 0.0) - self.ditta.serbatoi_ore.get("grado_A", 0.0), 2),
            "consumate_B": round(serbatoi_iniziali.get("grado_B", 0.0) - self.ditta.serbatoi_ore.get("grado_B", 0.0), 2)
        }

        report_stagionale["macchinari_interni_consumati"] = {
            "harvester": round(serbatoi_iniziali.get("harvester", 0.0) - self.ditta.serbatoi_ore.get("harvester", 0.0), 2),
            "forwarder": round(serbatoi_iniziali.get("forwarder", 0.0) - self.ditta.serbatoi_ore.get("forwarder", 0.0), 2),
            "trattori_alta": round(serbatoi_iniziali.get("trattori_alta", 0.0) - self.ditta.serbatoi_ore.get("trattori_alta", 0.0), 2),
            "trattori_media": round(serbatoi_iniziali.get("trattori_media", 0.0) - self.ditta.serbatoi_ore.get("trattori_media", 0.0), 2),
            "piattaforme": round(serbatoi_iniziali.get("piattaforme", 0.0) - self.ditta.serbatoi_ore.get("piattaforme", 0.0), 2)
        }

        report_stagionale["ricorso_terzi_e_noli"] = {
            chiave: round(self.ditta.registro_extra_anno.get(chiave, 0.0) - extra_iniziali.get(chiave, 0.0), 2)
            for chiave in ["grado_A", "grado_B", "trattori_alta", "trattori_media", "harvester", "forwarder", "piattaforme"]
        }

        return report_stagionale
    
    # Funzione che avanza di una stagione la simulazione, aggiornando lo stato dei lotti, eseguendo le lavorazioni 
    # restituendo un quadro completo dello stato attuale del pioppeto e dei risultati della stagione appena conclusa
    
    def avanza_passo_simulazione(self) -> Dict[str, Any]:
            
        if self.parametri.stagione_corrente == "Inverno":
            for lotto in self.parametri.collezione_lotti:
                profilo = self.dati_cloni[lotto.clone_assegnato]
                
                if lotto.eta == 0 and lotto.numero_piante_vive > 0:
                    lotto.eta = 1
                    lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                elif lotto.numero_piante_vive > 5: 
                    lotto.eta += 1
                    lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                
                lotto.diametro_medio_fusto = lotto.dati_correnti.get("dbh_reale_cm", 0.0)
                lotto.altezza_media_piante = lotto.dati_correnti.get("altezza_m", 0.0)
                if "piante_attive" in lotto.dati_correnti:
                    lotto.numero_piante_vive = lotto.dati_correnti["piante_attive"]
                lotto.malus_colturale_accumulato = 0.0

        # --- FOTOGRAFIA PRE-LAVORAZIONI (La Verità Biologica) ---
        stato_lotti_pre = {}
        for lotto in self.parametri.collezione_lotti:
            stato_lotti_pre[lotto.id_lotto] = {
                "eta": lotto.eta, 
                "tagliato": lotto.tagliato,
                "biometria": lotto.dati_correnti.copy() if hasattr(lotto, "dati_correnti") and lotto.dati_correnti else {
                    "dbh_reale_cm": 0.0, "altezza_m": 0.0, "volume_singolo_m3": 0.0, 
                    "piante_attive": lotto.numero_piante_vive, "volume_totale_m3": 0.0
                }
            }

        # --- ESECUZIONE CANTIERI ---
        risultati_cantieri = self.esegui_fase_lavorazioni_stagionali()

        # --- FOTOGRAFIA POST-LAVORAZIONI (Il nuovo punto di partenza) ---
        stato_lotti_istantaneo = {}
        for lotto in self.parametri.collezione_lotti:
            stato_lotti_istantaneo[lotto.id_lotto] = {
                "eta": lotto.eta, 
                "tagliato": lotto.tagliato,
                "biometria": lotto.dati_correnti.copy() if hasattr(lotto, "dati_correnti") and lotto.dati_correnti else {
                    "dbh_reale_cm": 0.0, "altezza_m": 0.0, "volume_singolo_m3": 0.0, 
                    "piante_attive": lotto.numero_piante_vive, "volume_totale_m3": 0.0
                }
            }

        if self.parametri.stagione_corrente == "Inverno":
            for lotto in self.parametri.collezione_lotti:
                if lotto.eta > 0:
                    profilo = self.dati_cloni[lotto.clone_assegnato]
                    eta_rot = 5 if lotto.destinazione_uso == "INDUSTRIA" else 10
                    
                    if lotto.eta >= eta_rot and not lotto.verifica_maturita_raccolta():
                        self.stats_globali["tagli_biologici_saltati"] += 1
                        lotto.anni_ritardo_taglio = getattr(lotto, "anni_ritardo_taglio", 0) + 1

            chiave_anno_storico = f"Anno_{self.parametri.anno_corrente}_RisorseExtra"
            if hasattr(self.parametri, "storico_stagionale"):
                self.parametri.storico_stagionale[chiave_anno_storico] = self.ditta.registro_extra_anno.copy()
            for risorsa in self.ditta.registro_extra_anno:
                self.ditta.registro_extra_anno[risorsa] = 0.0

        quadro_stato = {
            "risultati_cantieri": risultati_cantieri,
            "stato_lotti_pre": stato_lotti_pre,       # La nuova chiave per lo storico
            "stato_lotti": stato_lotti_istantaneo,    # La vecchia chiave per la retrocompatibilità
            "produzione_cumulata": {
                "opera_m3": getattr(self.parametri, "totale_prodotto_opera_m3", 0.0),
                "cartiera_t": getattr(self.parametri, "totale_prodotto_cartiera_t", 0.0),
                "truciolato_t": getattr(self.parametri, "totale_prodotto_truciolato_t", 0.0)
            }
        }
        
        if hasattr(self.parametri, "registra_instantanea_stato_corrente"):
            self.parametri.registra_instantanea_stato_corrente(quadro_stato)
        
        dati_orologio = self.parametri.avanza_stagione()
        return {**dati_orologio, **quadro_stato}