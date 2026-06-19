Gestione Pioppeto
Questo applicativo è stato sviluppato come parte del mio Project Work universitario. È un software dedicato alla modellazione e alla gestione tecnica di un pioppeto, pensato per supportare le decisioni operative in ambito forestale, dalla crescita biologica alla pianificazione dell'output industriale.

📋 Descrizione
L'applicativo utilizza un'architettura basata su Python per simulare l'accrescimento delle piante (modello di Richards) e calcolare la resa in termini di legname (sfogliati, cellulosa, biomassa), ottimizzando le risorse e le rotazioni colturali.

🚀 Come scaricare il progetto
Puoi ottenere una copia del progetto clonando la repository tramite Git o scaricandola come file ZIP.

Opzione 1: Clonazione tramite Git
Assicurati di avere Git installato sul tuo sistema, quindi apri il terminale e digita:

Bash
git clone https://github.com/Seyen75/Gestione_Pioppeto.git
cd gestione-pioppeto

Opzione 2: Download Archivio
Vai alla pagina principale della repository su GitHub.

Clicca sul pulsante verde "Code".

Seleziona "Download ZIP".

Estrai il contenuto in una cartella locale sul tuo PC.

🛠️ Requisiti di sistema
Per eseguire l'applicativo, è necessario avere installato:

Python 3.10+ (o versione compatibile)

PySide6 (per l'interfaccia grafica)

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

Logica: Modelli matematici per la crescita forestale (Equazione di Richards)

👤 Autore
Carubini Gabriele
