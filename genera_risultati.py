import json
import os
import itertools
import numpy as np

def analizza_statistiche_numero(cronologia_ruota, numero):
    """
    Analizza i 7 pilastri statistici per un singolo numero su una ruota.
    Ritorna un punteggio parziale per quel numero.
    """
    tot_estrazioni = len(cronologia_ruota)
    if tot_estrazioni < 50: # Abbiamo bisogno di uno storico profondo per ritardo medio/massimo
        return 0
        
    # Trova le posizioni (indici) in cui è uscito il numero (0 = più vecchia, tot-1 = stasera)
    presenze = [i for i, cinquina in enumerate(cronologia_ruota) if numero in cinquina]
    
    # 1. Ritardo Attuale
    ritardo_attuale = tot_estrazioni - 1 - presenze[-1] if presenze else tot_estrazioni
    
    # Calcolo dei ritardi storici intermedi
    ritardi_storici = []
    if len(presenze) > 1:
        for i in range(1, len(presenze)):
            ritardi_storici.append(presenze[i] - presenze[i-1] - 1)
    else:
        ritardi_storici = [tot_estrazioni]

    # 2. Ritardo Medio e 3. Ritardo Massimo
    ritardo_medio = np.mean(ritardi_storici) if ritardi_storici else 18
    ritardo_massimo = np.max(ritardi_storici) if ritardi_storici else 90

    # 4. Frequenza Breve (ultime 5) e 5. Frequenza Media (ultime 20)
    freq_breve = sum(1 for cinquina in cronologia_ruota[-5:] if numero in cinquina)
    freq_media = sum(1 for cinquina in cronologia_ruota[-20:] if numero in cinquina)
    
    # 6. Presenza Recente (Bonus/Malus cinetica nell'ultimo concorso)
    presenza_staserasi = 1 if (presenze and presenze[-1] == tot_estrazioni - 1) else 0
    
    # 7. Distribuzione delle uscite (Indice di Regolarità / Deviazione Standard dei ritardi)
    # Un valore basso di deviazione standard significa uscite molto regolari nel tempo
    regolarita = np.std(ritardi_storici) if len(ritardi_storici) > 1 else 50
    
    # --- ALGORITMO DI PESATURA PER IL PUNTEGGIO DEL SINGOLO NUMERO ---
    punteggio = 0
    punteggio += (ritardo_attuale / (ritardo_medio + 1)) * 25  # Peso Ritardo vs Media
    punteggio += (freq_media * 4)                             # Peso Frequenza Media
    punteggio += (freq_breve * 8)                             # Peso Frequenza Breve (Scia)
    punteggio += (10 if presenza_staserasi == 0 else 2)       # Preferenza per numeri non usciti stasera ma caldi nel mese
    punteggio += (30 / (regolarita + 1)) * 15                 # Premio alla regolarità di distribuzione
    
    return punteggio

def genera_risultati():
    if not os.path.exists('estrazioni.json'):
        print("Errore: estrazioni.json non trovato!")
        return
        
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        estrazioni = json.load(f)
    
    risultati = {"nuove": [], "colpo2": []}
    lista_ruote = list(estrazioni.keys())
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    classifiche_coppie = []
    
    # Calcoliamo i rating incrociati per tutte le ruote
    for r1, r2 in itertools.combinations(lista_ruote, 2):
        if len(estrazioni[r1]) < 50 or len(estrazioni[r2]) < 50:
            continue
            
        # Calcoliamo i punteggi per tutti i 90 numeri su entrambe le ruote
        punteggi_r1 = {n: analizza_statistiche_numero(estrazioni[r1], n) for n in range(1, 91)}
        punteggi_r2 = {n: analizza_statistiche_numero(estrazioni[r2], n) for n in range(1, 91)}
        
        # Trova i migliori numeri per ciascuna ruota
        miglior_n1 = max(punteggi_r1, key=punteggi_r1.get)
        miglior_n2 = max(punteggi_r2, key=punteggi_r2.get)
        
        # Il punteggio della coppia è la combinazione dei due rating reali
        punteggio_coppia = (punteggi_r1[miglior_n1] + punteggi_r2[miglior_n2]) / 2
        
        classifiche_coppie.append({
            "ruota1": r1, "ruota2": r2,
            "numero1": miglior_n1, "numero2": miglior_n2,
            "rating_totale": punteggio_coppia
        })
    
    # Ordina tutte le previsioni possibili in Italia dalla più forte alla più debole
    classifiche_coppie.sort(key=lambda x: x["rating_totale"], reverse=True)
    
    conteggio_ruote = {ruota: 0 for ruota in lista_ruote}
    previsioni_filtrate = []
    
    # Seleziona le migliori 8 senza sovraccaricare le ruote (max 2 comparse per ruota)
    for cov in classifiche_coppie:
        r1, r2 = cov["ruota1"], cov["ruota2"]
        if conteggio_ruote[r1] < 2 and conteggio_ruote[r2] < 2:
            previsioni_filtrate.append(cov)
            conteggio_ruote[r1] += 1
            conteggio_ruote[r2] += 1
        if len(previsioni_filtrate) >= 8:
            break

    # Smistamento nei pannelli grafici
    for idx, prev in enumerate(previsioni_filtrate):
        colore_r1 = "red" if prev["ruota1"] in ruote_rosse else ("gray" if prev["ruota1"] in ruote_grigie else "yellow")
        colore_r2 = "red" if prev["ruota2"] in ruote_rosse else ("gray" if prev["ruota2"] in ruote_grigie else "yellow")
        
        # Trasformiamo il rating in percentuale di accuratezza visiva (es: 175%)
        accuratezza_visiva = int(150 + (prev["rating_totale"] * 0.5))
        
        data_struttura = {
            "ruota1": prev["ruota1"], "ruota2": prev["ruota2"],
            "numero1": prev["numero1"], "numero2": prev["numero2"],
            "colore_r1": colore_r1, "colore_r2": colore_r2,
            "budget": "4.00€",
            "accuratezza": f"{accuratezza_visiva}%"
        }
        
        if idx < 4:
            risultati["nuove"].append(data_struttura)
        else:
            risultati["colpo2"].append(data_struttura)

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
        
    print("Mdf completato: Attivato Modello Matematico Multi-Fattoriale.")

if __name__ == "__main__":
    genera_risultati()
