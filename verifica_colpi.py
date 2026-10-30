import json
import os

def controlla_esiti():
    # 1. Caricamento del file dei risultati correnti
    if not os.path.exists('risultati_v4.json'):
        print("Errore: Il file risultati_v4.json non esiste. Esegui prima genera_risultati.py")
        return
        
    with open('risultati_v4.json', 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    # 2. Caricamento dell'archivio estrazioni storico per estrarre l'ultimo concorso
    if not os.path.exists('estrazioni.json'):
        print("Errore: Il file estrazioni.json non esiste. Impossibile verificare i colpi.")
        return
        
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio_estrazioni = json.load(f)
    
    # Estrae l'ultima cinquina inserita nell'archivio per la ruota di BARI
    # Assumiamo che l'archivio contenga una lista o un dizionario con l'ultima estrazione in fondo o indicizzata
    try:
        # Adatta questa riga alla struttura reale del tuo estrazioni.json
        # Qui simuliamo il recupero dell'ultima estrazione di Bari inserita (es: quella del 29/10/2026)
        if isinstance(archivio_estrazioni, list):
            ultima_estrazione = archivio_estrazioni[-1]
            # Se la struttura è una lista di dizionari con chiavi data e ruote
            data_estrazione = ultima_estrazione.get("data", "")
            cinquina_reale = ultima_estrazione.get("BARI", [])
        elif "BARI" in archivio_estrazioni:
            # Se è strutturato per ruota direttamente
            data_estrazione = archivio_estrazioni.get("ultima_data", "")
            cinquina_reale = archivio_estrazioni["BARI"]
        else:
            print("Struttura estrazioni.json non riconosciuta automaticamente.")
            return
    except Exception as e:
        print(f"Errore nella lettura di estrazioni.json: {e}")
        return

    if not cinquina_reale:
        print("Nessuna cinquina trovata per BARI nell'ultima estrazione.")
        return

    # Convertiamo i numeri in stringhe/interi per il confronto pulito
    cinquina_interi = [int(x) for x in cinquina_reale]
    cinquina_str = "-".join(map(str, cinquina_interi))
    
    ambata_target = int(database["previsione_corrente"]["ambata"])
    ambi_target = database["previsione_corrente"]["ambi_secchi"] # Lista di stringhe formato "8-53"

    print(f"Verifica concorso del {data_estrazione} su BARI: {cinquina_str}")
    print(f"Previsione da controllare -> Ambata: {ambata_target} | Ambi: {ambi_target}")

    aggiornato = False

    # 3. Scansione della tabella colpi per trovare lo slot attivo da chiudere
    for i, colpo in enumerate(database["tabella_colpi"]):
        if colpo["stato"] == "In corso":
            # Registriamo i dati reali su questo colpo
            colpo["cinquina"] = cinquina_str
            
            # Verifica Ambata
            if ambata_target in cinquina_interi:
                colpo["esito_ambata"] = "VINCENTE"
            else:
                colpo["esito_ambata"] = "Negativo"
                
            # Verifica Ambi Secchi
            ambi_vinti = []
            for ambo in ambi_target:
                n1, n2 = map(int, ambo.split('-'))
                if n1 in cinquina_interi and n2 in cinquina_interi:
                    ambi_vinti.append(ambo)
            
            if ambi_vinti:
                colpo["esito_ambi"] = f"VINCENTE ({', '.join(ambi_vinti)})"
            else:
                colpo["esito_ambi"] = "Negativo"
                
            colpo["stato"] = "Chiuso"
            aggiornato = True
            
            # Attiviamo il colpo successivo se presente nella finestra dei 6 colpi
            if i + 1 < len(database["tabella_colpi"]):
                database["tabella_colpi"][i + 1]["stato"] = "In corso"
            break

    if aggiornato:
        # Salva le modifiche nel file risultati_v4.json
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
        print("File risultati_v4.json aggiornato con successo! Ricarica la dashboard.")
    else:
        print("Nessun colpo contrassegnato come 'In corso' o nessun nuovo dato da aggiornare.")

if __name__ == "__main__":
    controlla_esiti()
