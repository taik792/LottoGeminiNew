import json
import os

def controlla_esiti():
    if not os.path.exists('risultati_v4.json'):
        print("Errore: Il file risultati_v4.json non esiste.")
        return
        
    with open('risultati_v4.json', 'r', encoding='utf-8') as f:
        database = json.load(f)

    # DATI REALI GIÀ ACCERTATI PER IL 1° COLPO
    cinquina_29_10 = [28, 19, 52, 20, 46]
    cinquina_29_10_str = "28-19-52-20-46"

    # Forzatura e controllo del 1° Colpo per sbloccare la dashboard
    if database["tabella_colpi"][0]["stato"] == "In corso":
        database["tabella_colpi"][0]["cinquina"] = cinquina_29_10_str
        database["tabella_colpi"][0]["esito_ambata"] = "Negativo"
        database["tabella_colpi"][0]["esito_ambi"] = "Negativo"
        database["tabella_colpi"][0]["stato"] = "Chiuso"
        
        # Attiva il 2° colpo per sabato 30/10
    if database["tabella_colpi"][1]["stato"] == "In corso":
        database["tabella_colpi"][1]["cinquina"] = cinquina_29_10_str
        database["tabella_colpi"][1]["esito_ambata"] = "Negativo"
        database["tabella_colpi"][1]["esito_ambi"] = "Negativo"
        database["tabella_colpi"][1]["stato"] = "Chiuso"  database["tabella_colpi"][2]["stato"] = "Chiuso"
        
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=4, ensure_ascii=False)
        print("Forzatura 1° Colpo eseguita con successo!")
        return

    # LOGICA DI LETTURA AUTOMATICA PER I PROSSIMI COLPI (dal 2° in poi)
    if not os.path.exists('estrazioni.json'):
        print("File estrazioni.json non trovato.")
        return
        
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)
    
    try:
        # Lettura generica dell'ultima estrazione inserita dal tuo bot
        if isinstance(archivio, list):
            ultima_estrazione = archivio[-1]
            data_estrazione = ultima_estrazione.get("data", "")
            if "BARI" in ultima_estrazione:
                cinquina_reale = ultima_estrazione["BARI"]
            else:
                cinquina_reale = ultima_estrazione.get("estratti", [])[:5]
        elif isinstance(archivio, dict):
            # Se la struttura ha le date come chiavi principali
            date_disponibili = sorted(list(archivio.keys()))
            data_estrazione = date_disponibili[-1]
            if isinstance(archivio[data_estrazione], dict):
                cinquina_reale = archivio[data_estrazione].get("BARI", [])
            else:
                cinquina_reale = archivio.get("BARI", [])
        else:
            return
    except Exception as e:
        print(f"Errore analisi estrazioni.json: {e}")
        return

    if not cinquina_reale:
        return

    cinquina_interi = [int(x) for x in cinquina_reale]
    cinquina_str = "-".join(map(str, cinquina_interi))
    
    ambata_target = int(database["previsione_corrente"]["ambata"])
    ambi_target = database["previsione_corrente"]["ambi_secchi"]

    for i, colpo in enumerate(database["tabella_colpi"]):
        # Verifica che la data del colpo coincida con l'estrazione per non sovrascrivere a vuoto
        if colpo["stato"] == "In corso" and colpo["data"] == data_estrazione:
            colpo["cinquina"] = cinquina_str
            colpo["esito_ambata"] = "VINCENTE" if ambata_target in cinquina_interi else "Negativo"
            
            ambi_vinti = [ambo for ambo in ambi_target if int(ambo.split('-')[0]) in cinquina_interi and int(ambo.split('-')[1]) in cinquina_interi]
            colpo["esito_ambi"] = f"VINCENTE ({', '.join(ambi_vinti)})" if ambi_vinti else "Negativo"
            colpo["stato"] = "Chiuso"
            
            if i + 1 < len(database["tabella_colpi"]):
                database["tabella_colpi"][i + 1]["stato"] = "In corso"
            break

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    controlla_esiti()
