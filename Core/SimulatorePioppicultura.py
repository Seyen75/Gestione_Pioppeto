import os
import json

from typing import Dict, List, Any
from Core.struttura_lavorazioni import STRUTTURA_LAVORAZIONI
from Core.gestori_clone import GestoreCloni

class SimulatorePioppicoltura:
    def __init__(self, ditta: Any, parametri: Any):
        self.ditta = ditta
        self.parametri = parametri  
        self.gestore_cloni = GestoreCloni()
        self.dati_cloni = self.gestore_cloni.carica_cloni()


    def prevedi_domanda_stagionale(self, is_esecuzione: bool = False) -> List[Dict[str, Any]]:
        '''Funzione che crea la lista degli interventi che sono previsti per la stagione che è in corso di simulazione'''
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
            is_maturo = lotto.verifica_maturita_raccolta(self.parametri.tolleranza_taglio)
            
            # Ripristino immediato dello stato originale per non corrompere la simulazione
            lotto.eta = eta_originale
            lotto.diametro_medio_fusto = diametro_originale

            
            # inserisce nella variabile filiera la lista di lavorazioni previste per la tipologia di destinazione d'uso, OPERA o INDUSTRIA 
            filiera = STRUTTURA_LAVORAZIONI[lotto.destinazione_uso]
            
            # Controllo che verifica lo stato del lotto. Se è maturo e non è stato tagliato allora mette fra le operazioni
            # da fare presenti nella lista. Se è inverno non deve fare alcuna operazione perchè ci sarà raccolta
            if is_maturo or lotto.tagliato:  
                if stagione == "Inverno":
                    # Verifichiamo la presenza della "flotta pesante" (Proprietà + Mercato Noli)
                    harvesters = self.ditta.harvester_abbattitori + self.ditta.limiti_noli_stagionali["harvester"]
                    forwarders = self.ditta.forwarder_caricatori + self.ditta.limiti_noli_stagionali["forwarder"]
                    cippatrici = self.ditta.cippatrice + self.ditta.limiti_noli_stagionali["cippatrice"]

                    if harvesters > 0 or forwarders > 0 or cippatrici > 0:
                        # Tutto ok, si procede con la raccolta avanzata da filiera (OP_RAC_01 o OP_RAC_02)
                        ops = filiera["Raccolta"]["Inverno"]
                    else:
                        # Mancano i mezzi: si dirotta forzatamente sulla raccolta tradizionale
                        # Assicurati che OP_RAC_03 sia importato/disponibile in questo modulo
                        ops = filiera["Raccolta_tradizionale"]["Inverno"]
                else:
                    ops = []
                    
                is_raccolta = (stagione == "Inverno")

            # se non è maturo o tagliato allora carica fra le operazioni quelle di mantenimento
            else:
                f_k = lotto.get_fase_colturale()
                ops = filiera.get(str(f_k), {}).get(stagione, []) if f_k is not None else []
                is_raccolta = False
            
            
            # Trasforma la lista di operazioni teoriche ops in un preventivo tecnico dettagliato (interventi), calcolando quanto lavoro serve, con quali macchine e per quale superficie.
            for op in ops:
                id_univoco = op["id_operazione"]
                
                descrizione_ui = op["descrizione"]
                macrocategoria = op["macrocategoria"]
                
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
                ore_ettaro = op["ore_ha"]
                squadra = op["risorse"]
                
                # avvia la funzione che calcola le specifiche del cantiere per le specifiche
                # fornisce oltre i dati ottenuti prima anche l'indice di attrito spaziale del lotto, che indica le difficoltà tecniche del lotto
                # per la sua morfologia (pendenza del terreno, vicinanza alla strada, accessibilità, etc). 
                # L'unità_lavoro è specifica per la macrocategoria, numero piante per raccolta, ettari per le altre operazioni, in modo da adattare il calcolo alle specificità di ogni tipo di lavorazione 
                spec = self.ditta.calcola_specifiche_richiesta_cantiere(
                    tipo_cantiere = macrocategoria, 
                    unita_lavoro = unita, 
                    ore_unitarie = ore_ettaro,
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
        return sorted(
            interventi, 
            key=lambda x: (
                x["priorita"], 
                0 if str(x["lotto"].destinazione_uso) == "OPERA" else 1, 
                -x["lotto"].superficie_ettari 
            )
        )

    
    def esegui_fase_lavorazioni_stagionali(self) -> Dict[str, Any]:
        '''Funzione che esegue le lavorazioni necessarie per la stagione da simulare.
           Ottiene le lista delle lavorazioni e crea un dizionario di risposta con il report stagionale delle attività svolte
           che sarà utilizzato per la reportistica di fine simulazione'''
         
        # Inizia la variabile locale con i dati dei parametri della stagione corrente ed inizializza i serbatoi stagionali della ditta
        stagione_attiva = self.parametri.stagione_corrente
        giornate_lavorative = 55
        self.ditta.inizializza_serbatoi_stagionali(giornate_lavorative)
        
        # Crea una copia dei serbatoi della ditta per calcolare i consumi effettivi a fine stagione per differenza
        serbatoi_iniziali = self.ditta.serbatoi_ore.copy()
        extra_iniziali = self.ditta.registro_extra_anno.copy()
        
        # Inizializza all'interno del dizionario del report stagionale le due liste
        report_stagionale = {"dettaglio_operazioni": [], "tagli_effettuati": []}
        
        # Crea il dizionario dei fallimenti stagionali delle lavorazioni suddivise in fallimenti biologici (lotto non maturi) e di lavorazioni (manacanza risorse per i lavori)
        fallimenti = {
            "tagli": {"rinviati_maturita": 0, "saltati_risorse": 0},
            "lavorazioni_generiche": {"saltate_risorse": 0}
        }
        
        # Genera la lista pianificata degli interventi per la stagione corrente
        lista_interventi = self.prevedi_domanda_stagionale(is_esecuzione=True)
    
        # Ciclo completo di esecuzione per tutte le lavorazioni in lista
        for intervento in lista_interventi:
            lotto = intervento["lotto"]
            spec = intervento["specifiche_richiesta"]
            
            # Verifica e consuma le ore/risorse della ditta, ottenendo la percentuale di completamento dell'opera
            perc = self.ditta.verifica_e_consuma_risorse(spec)
    
            # --- 1. GESTIONE RACCOLTA (Avviene SOLO in Inverno) ---
            if intervento["is_raccolta"] and intervento["tipo_cantiere_chiave"] == "raccolta":
                
                # Fallito il taglio per mancanza risorse, l'accumulatore viene incrementato
                if perc <= 0.001:
                    fallimenti["tagli"]["saltati_risorse"] += 1
                
                # Conteggia il numero di piante abbattute in base alla percentuale di completamento del cantiere
                p_abbattute = int(lotto.dati_correnti["piante_attive"] * perc)
                
                # Calcola le rese e aggiorna lo stato interno delle piante nel lotto
                rese, stato = lotto.esegui_raccolta(p_abbattute, self.dati_cloni[lotto.clone_assegnato])
                
                if "Reset Ciclo" in stato:
                    # Viene azzerata l'età del lotto tagliato
                    lotto.eta = 0 
                else:
                    # TAGLIO PARZIALE INVERNALE: 
                    # Aggiorna solo il volume totale in base alle piante rimaste in piedi.
                    lotto.dati_correnti["piante_attive"] = lotto.numero_piante_vive
                    lotto.dati_correnti["volume_totale_m3"] = round(
                        lotto.dati_correnti.get("volume_singolo_m3", 0.0) * lotto.numero_piante_vive, 2
                    )
                
                # Aggiorna i contatori comprensoriali globali se sono state abbattute piante
                if p_abbattute > 0:
                    # Registra i dati specifici della resa del lotto nel report
                    report_stagionale["tagli_effettuati"].append({
                        "lotto_id": lotto.id_lotto, 
                        "rese": rese
                    })
            
            # --- 2. GESTIONE LAVORAZIONI DI MANUTENZIONE (Primavera, Estate, Autunno) ---
            else:
                # Fallita la lavorazione diversa dal taglio per mancanza risorse 
                if perc <= 0.001:
                    fallimenti["lavorazioni_generiche"]["saltate_risorse"] += 1
                    
                # Applica la lavorazione al lotto e accumula l'eventuale malus se fallisce
                stato = lotto.applica_lavorazione(
                    intervento["operazione"], intervento["tipo_cantiere_chiave"], perc, 
                    stagione_attiva, self.parametri.anno_corrente, 
                    self.dati_cloni[lotto.clone_assegnato], intervento["priorita"]
                )

            # Popolamento dei dati consuntivi sulle ore e sull'efficienza per il report comune
            ore_teoriche = spec.get("meta_lavoro_puro", 0.0) / self.ditta.coefficiente_rendimento_cantiere
            report_stagionale["dettaglio_operazioni"].append({
                "lotto_id": lotto.id_lotto, 
                "id_operazione": intervento["id_operazione"], 
                "durata_cantiere_h": round(spec.get("ore_richieste", 0.0), 2),
                "ore_lavoro_totali": round(ore_teoriche * perc, 2),
                "percentuale_completamento": round(perc * 100, 2),
                "squadre_attive": spec.get("meta_linee_attive", 1),
                "stato": stato
            })
    
        # Viene avviato un controllo per verificare se ci sono stati lotti in età da taglio che per motivi biologici non hanno raggiunto la giusta maturità
        if stagione_attiva == "Inverno":
            for lotto_bio in self.parametri.collezione_lotti:
                eta_rot = 5 if lotto_bio.destinazione_uso == "INDUSTRIA" else 10
                # Se il lotto ha l'età da taglio, non è ancora tagliato, ma non ha il diametro sufficiente
                
                if lotto_bio.eta >= eta_rot and not lotto_bio.tagliato and not lotto_bio.verifica_maturita_raccolta(self.parametri.tolleranza_taglio):
                    fallimenti["tagli"]["rinviati_maturita"] += 1

        report_stagionale["fallimenti_lavorazioni"] = fallimenti
        
        # Genera il bilancio finale confrontando lo stato finale dei serbatoi con quello iniziale
        report_finale = self.ditta.genera_report_consumi(serbatoi_iniziali, extra_iniziali)
        
        # Unisce i dati dei consumi ditta con i registri delle operazioni dei lotti e restituisce il dizionario fuso
        return {**report_finale, **report_stagionale}
    
    
    def avanza_passo_simulazione(self) -> Dict[str, Any]:
        ''' Funzione regista della simulazione.
            Questa avanza di una stagione la simulazione, eseguendo tutte le operazioni necessarie per la stagione corrente e aggiornando lo stato dei lotti e della ditta.
            Ritorna un dizionario con lo stato aggiornato della simulazione, utilizzato per la reportistica finale e per l'aggiornamento dell'interfaccia utente.'''
        
        # Se la stagione è l'inverno, ultima stagione dell'anno biologico, viene effettuato l'avanzamento biologico dei lotti
        if self.parametri.stagione_corrente == "Inverno":
            for lotto in self.parametri.collezione_lotti:
                profilo = self.dati_cloni[lotto.clone_assegnato]
                
                # Invecchiamento e calcolo accrescimento
                if lotto.eta == 0 and lotto.numero_piante_vive > 0:
                    lotto.eta = 1
                    lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                elif lotto.numero_piante_vive > 5: 
                    lotto.eta += 1
                    lotto.dati_correnti = lotto.simula_accrescimento(profilo, lotto.eta)
                
                # Sincronizzazione attributi del Lotto
                lotto.diametro_medio_fusto = lotto.dati_correnti["dbh_reale_cm"]
                lotto.altezza_media_piante = lotto.dati_correnti["altezza_m"]   
                lotto.numero_piante_vive = lotto.dati_correnti["piante_attive"]
                lotto.malus_colturale_accumulato = 0.0

        # Salva i dati dello stato dei lotti prima delle operazioni nel dizionario da aggiungere poi nel report stagionale
        
        stato_lotti_pre = {}
        for lotto in self.parametri.collezione_lotti:
            stato_lotti_pre[lotto.id_lotto] = {
                "eta": lotto.eta, 
                "tagliato": lotto.tagliato,
                "biometria": lotto.dati_correnti.copy() if hasattr(lotto, "dati_correnti") else {}
            }

        # Si manda in esecuzione la stagione con le varie funzioni collegate
        risultati_cantieri = self.esegui_fase_lavorazioni_stagionali()

        # Gestisce se siamo in inverno (stagione finale dell'anno selvicolturale) l'aumento della variabile degli anni di ritardo
        # taglio di un lotto che ha raggiunto l'età del taglio ma non ha il diametro adeguato
        if self.parametri.stagione_corrente == "Inverno":
            for lotto in self.parametri.collezione_lotti:
                if lotto.eta > 0:
                    eta_rot = 5 if lotto.destinazione_uso == "INDUSTRIA" else 10
                    if lotto.eta >= eta_rot and not lotto.verifica_maturita_raccolta(self.parametri.tolleranza_taglio):
                        lotto.anni_ritardo_taglio = getattr(lotto, "anni_ritardo_taglio", 0) + 1

            # Salva i totali dell'anno di tutti i valori delle ore di operai stagionali e noli strumentazioni, utilizzati poi nella reportistica
            chiave_anno_storico = f"Anno_{self.parametri.anno_corrente}_RisorseExtra"
            self.parametri.storico_stagionale[chiave_anno_storico] = self.ditta.registro_extra_anno.copy()
            
            
            for risorsa in self.ditta.registro_extra_anno:
                self.ditta.registro_extra_anno[risorsa] = 0.0

        # Aggiunge i dizionari dei risultati cantieri e dello stato dei lotti creati precedentemente
        quadro_stato = {
            "risultati_cantieri": risultati_cantieri,
            "stato_lotti_pre": stato_lotti_pre
        }
        
        # Registra lo stato corrente
        self.parametri.registra_instantanea_stato_corrente(quadro_stato)

        # Avanza la stagione e restituisce i dati 
        dati_stagione = self.parametri.avanza_stagione()
        return {**dati_stagione, **quadro_stato}