Gestione Pioppeto
Questo applicativo è stato sviluppato come parte del mio Project Work universitario. È un software dedicato alla modellazione e alla gestione tecnica di un pioppeto, pensato per supportare le decisioni operative in ambito forestale, dalla crescita biologica alla pianificazione dell'output industriale.

📋 Descrizione
L'applicativo utilizza un'architettura basata su Python per simulare l'accrescimento delle piante (modello di Richards) e calcolare la resa in termini di legname (sfogliati, cellulosa, biomassa), ottimizzando le risorse e le rotazioni colturali.

🚀 Come scaricare il progetto
Puoi ottenere una copia del progetto clonando la repository tramite Git o scaricandola come file ZIP.

- Opzione 1: Clonazione tramite Git
    Assicurati di avere Git installato sul tuo sistema, quindi apri il terminale e digita:
    
    Bash
    
    git clone https://github.com/Seyen75/Gestione_Pioppeto.git
    
    cd gestione-pioppeto

- Opzione 2: Download Archivio
    Vai alla pagina principale della repository su GitHub.
    
    Clicca sul pulsante verde "Code".
    
    Seleziona "Download ZIP".
    
    Estrai il contenuto in una cartella locale sul tuo PC.

🛠️ Requisiti di sistema
Per eseguire l'applicativo, è necessario avere installato:

- Python 3.10+ (o versione compatibile)

- PySide6 (per l'interfaccia grafica)

💻 Come rendere l'applicativo eseguibile in locale
Per configurare l'ambiente e avviare il software, segui questi passaggi:

1. Creazione dell'ambiente virtuale (Consigliato)
È buona norma isolare le dipendenze del progetto. Apri il terminale nella cartella del progetto ed esegui:

    Bash
    
    # Crea l'ambiente virtuale
    
    python -m venv venv
    
    # Attiva l'ambiente virtuale
    # Su Windows:
    
    venv\Scripts\activate
    
    # Su macOS/Linux:
    
    source venv/bin/activate

2. Installazione delle dipendenze
Installa le librerie necessarie elencate nel file requirements.txt:

    Bash

    pip install -r requirements.txt

3. Esecuzione
    Una volta completata l'installazione, puoi avviare l'applicativo lanciando lo script principale:
    
    Bash
    
    python main.py

📈 Tecnologie utilizzate
Linguaggio: Python

Interfaccia Grafica: PySide6 


L'interfaccia "Azienda Pioppicola Padana" è strutturata con sei pulsanti operativi che guidano l'utente attraverso le fasi della simulazione:

- Configurazione Ditta Forestale: Consente di modificare e inventariare i mezzi meccanici e le squadre reali della ditta. Questi dati determinano la capacità oraria operativa e influenzano la necessità di personale stagionale o noleggio mezzi.

- Gestione e Creazione Lotti: Permette la creazione e la modifica selvicolturale dei lotti. Include la parametrizzazione dei Cloni Padani, la valutazione della vulnerabilità idrica e dell'attrito logistico, e la scelta dell'indirizzo produttivo (Opera o Industria).

- Avvia Simulazione: Avvia l'algoritmo di simulazione automatica. Il calcolo procede per stagioni biologiche, eseguendo i cantieri con relativo consumo ore e chiudendo automaticamente il ciclo al completamento.

- Monitoraggio Grafico Real-Time: Fornisce una visualizzazione dinamica e in tempo reale dell'avanzamento dei cicli in campo. Mostra l'accrescimento dendrometrico, la saturazione dei serbatoi e l'insorgenza di anomalie o stress idrici.

- Report Finale e Statistiche Consuntive: Fornisce l'analisi scientifica dei risultati economici e forestali a fine simulazione: cubature (m³), masse in fibra (t), rese ettariali ed efficienza del capitale meccanico ed umano.

- Reset Simulazione: Cancella ogni dato precedentemente inserito per la simulazione corrente, permettendo di configurare una nuova ditta e nuovi lotti da zero.


👤 Autore
Carubini Gabriele
