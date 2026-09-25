import json
import os

def fuori_90(numero):
    while numero > 90: numero -= 90
    while numero <= 0: numero += 90
    return numero

def calcola_diametrale(numero):
    if numero <= 45: return numero + 45
    return numero - 45

def super_ottimizzazione_globale():
    if not os.path.exists('estrazioni.json'):
        print("Errore: estrazioni.json non trovato.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    archivio_pulito = {k.upper(): v for k, v in archivio.items() if isinstance(v, list) and len(v) > 0}
    ruote_disponibili = [r for r in archivio_pulito.keys() if r != "NAZIONALE"]
    
    if not ruote_disponibili:
        print("Nessuna ruota valida trovata nell'archivio.")
        return

    # Usiamo una ruota qualsiasi per contare le estrazioni totali
    prima_ruota = list(archivio_pulito.keys())[0]
    tot_estrazioni = len(archivio_pulito[prima_ruota])
    classifica_combinazioni = []

    print(f"🔬 SUPER OTTIMIZZAZIONE GLOBALE SU {tot_estrazioni} ESTRAZIONI...")
    print("Analisi di 9.000 combinazioni in corso (Tutte le ruote x Tutti i 90 Fissi)...")

    # Ciclo incrociato su TUTTE le ruote possibili
    for r_base in ruote_disponibili:
        estrazioni_base = archivio_pulito[r_base]
        
        for r_recupero in ruote_disponibili:
            if r_base == r_recupero: continue
            estrazioni_recupero = archivio_pulito[r_recupero]
            
            # Test di tutti i 90 fissi per questa specifica coppia
            for fisso in range(1, 91):
                vincite_ambata = 0
                vincite_ambo = 0
                totale_previsioni = 0

                for i in range(tot_estrazioni - 9):
                    if i >= len(estrazioni_recupero) or i >= len(estrazioni_base): break
                    if not estrazioni_base[i] or len(estrazioni_base[i]) < 1: continue
                    
                    try:
                        primo_numero = int(estrazioni_base[i]) if isinstance(estrazioni_base[i], list) else int(estrazioni_base[i])
                        ambata = fuori_90(primo_numero + fisso)
                        abbinamento = calcola_diametrale(ambata)
                        
                        totale_previsioni += 1
                        vinta_ambata = False
                        vinto_ambo = False

                        for colpo in range(1, 10):
                            idx = i + colpo
                            if idx >= tot_estrazioni or idx >= len(estrazioni_recupero): break
                            
                            num_base_futuri = [int(n) for n in estrazioni_base[idx][:5]]
                            num_recu_futuri = [int(n) for n in estrazioni_recupero[idx][:5]]

                            if not vinta_ambata and ((ambata in num_base_futuri) or (ambata in num_recu_futuri)):
                                vincite_ambata += 1
                                vinta_ambata = True

                            if not vinto_ambo:
                                if (ambata in num_base_futuri and abbinamento in num_base_futuri) or (ambata in num_recu_futuri and abbinamento in num_recu_futuri):
                                    vincite_ambo += 1
                                    vinto_ambo = True
                    except:
                        continue

                if totale_previsioni > 0 and vincite_ambo > 0:
                    p_ambata = (vincite_ambata / totale_previsioni) * 100
                    p_ambo = (vincite_ambo / totale_previsioni) * 100
                    
                    classifica_combinazioni.append({
                        "ruota_1": r_base,
                        "ruota_2": r_recupero,
                        "fisso": fisso,
                        "perc_ambata": p_ambata,
                        "perc_ambo": p_ambo,
                        "ambi_totali": vincite_ambo,
                        "tot_prev": totale_previsioni
                    })

    # Ordina la classifica per la percentuale di Ambi Secchi vinti
    classifica_combinazioni.sort(key=lambda x: x["perc_ambo"], reverse=True)
    top_5 = classifica_combinazioni[:5]

    # STAMPA A SCHERMO PER I LOG DI GITHUB
    print("=" * 70)
    print("🏆 CLASSIFICA ASSOLUTA TOP 5 - LOTTO INTELLIGENCE V8 🏆")
    print("=" * 70)
    for idx, combo in enumerate(top_5, 1):
        print(f"{idx}° POSTO: {combo['ruota_1']} - {combo['ruota_2']} | Fisso: +{combo['fisso']}")
        print(f"   Ambata: {combo['perc_ambata']:.2f}% | Ambi Vinti: {combo['ambi_totali']} ({combo['perc_ambo']:.2f}%)")
        print("-" * 70)

if __name__ == "__main__":
    super_ottimizzazione_globale()
