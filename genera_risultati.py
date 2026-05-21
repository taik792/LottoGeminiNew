import json
import os
from collections import Counter

def calcola_distanza(n1, n2):
    """Calcola la distanza ciclometrica (max 45)"""
    dist = abs(n1 - n2)
    if dist > 45:
        dist = 90 - dist
    return dist

def analizza_tendenza_laterale(archivio, chiavi_ordinate, numero_teorico, ruota, colpi_indietro=30):
    """
    Passo 2: Analizza la cronologia passata per vedere se la ruota 
    tende a sfornare il numero laterale (+1/-1) invece di quello secco.
    """
    if len(chiavi_ordinate) < 2:
        return False
    
    uscite_laterali = 0
    uscite_secche = 0
    
    # Numeri laterali con gestione del ciclo dei 90 numeri
    lat_meno = 90 if numero_teorico == 1 else numero_teorico - 1
    lat_piu = 1 if numero_teorico == 90 else numero_teorico + 1
    
    # Esaminiamo la cronologia recente della ruota
    estrazioni_da_controllare = chiavi_ordinate[-colpi_indietro-1:-1]
    for data in estrazioni_da_controllare:
        if ruota in archivio[data]:
            numeri_estratti = archivio[data][ruota]
            if numero_teorico in numeri_estratti:
                uscite_secche += 1
            if lat_meno in numeri_estratti or lat_piu in numeri_estratti:
                uscite_laterali += 1
                
    # Se il numero laterale esce significativamente più del secco, segnala la tendenza
    return uscite_laterali > uscite_secche and uscite_laterali > 0

def genera_risultati():
    # 1. Caricamento dell'archivio estrazioni
    if not os.path.exists('estrazioni.json'):
        print("Errore: file estrazioni.json non trovato.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    chiavi_ordinate = sorted(list(archivio.keys()))
    if len(chiavi_ordinate) < 1:
        print("Errore: l'archivio non contiene abbastanza estrazioni.")
        return

    # Struttura dati finale (mantiene la compatibilità con la V4 per la dashboard)
    risultati = {
        "nuove": [],
        "colpo2": [],
        "colpo3": [],
        "mappa_calore": {}  # <-- PASSO 3: Nuova sezione per i dati di calore delle ruote
    }

    mappa_colpi = {
        "nuove": chiavi_ordinate[-1] if len(chiavi_ordinate) >= 1 else None,
        "colpo2": chiavi_ordinate[-2] if len(chiavi_ordinate) >= 2 else None,
        "colpo3": chiavi_ordinate[-3] if len(chiavi_ordinate) >= 3 else None
    }

    # Elenco ruote stabili (esclusa Nazionale per bilanciamento ciclometrico)
    elenco_ruote_valide = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

    # 2. Elaborazione per ciascun colpo
    for etichetta_colpo, data_estrazione in mappa_colpi.items():
        if not data_estrazione:
            continue

        estrazione_corrente = archivio[data_estrazione]
        card_temporanee = []
        ruote_rilevate_nel_colpo = []

        # Confronto tra tutte le coppie di ruote (Isotopia e Simmetria)
        for i in range(len(elenco_ruote_valide)):
            for j in range(i + 1, len(elenco_ruote_valide)):
                ruota1 = elenco_ruote_valide[i]
                ruota2 = elenco_ruote_valide[j]

                if ruota1 not in estrazione_corrente or ruota2 not in estrazione_corrente:
                    continue

                num_r1 = estrazione_corrente[ruota1]
                num_r2 = estrazione_corrente[ruota2]

                for pos in range(5):
                    n1 = num_r1[pos]
                    n2 = num_r2[pos]

                    dist = calcola_distanza(n1, n2)

                    # Distanze armoniche di verifica
                    if dist in [45, 30, 15]:
                        score = 172
                        if dist == 45:
                            score = 180

                        pronostico_1 = (n1 + 30) % 90
                        pronostico_2 = (n2 + 30) % 90
                        if pronostico_1 == 0: pronostico_1 = 90
                        if pronostico_2 == 0: pronostico_2 = 90

                        # =======================================================
                        # CORREZIONE AUTOMATICA ANOMALIE IDENTICHE (Es: 45 - 45)
                        # =======================================================
                        if pronostico_1 == pronostico_2:
                            if pronostico_1 <= 45:
                                pronostico_2 = pronostico_1 + 45
                            else:
                                pronostico_2 = pronostico_1 - 45

                        # =======================================================
                        # 🛠️ PASSO 2: CONTROLLO ABITUDINI DI ERRORE (+1 / -1)
                        # =======================================================
                        tendenza_r1 = analizza_tendenza_laterale(archivio, chiavi_ordinate, pronostico_1, ruota1)
                        tendenza_r2 = analizza_tendenza_laterale(archivio, chiavi_ordinate, pronostico_2, ruota2)
                        
                        nota_correttiva = ""
                        if tendenza_r1 or tendenza_r2:
                            nota_correttiva = "Consigliata copertura laterale (+1/-1)"

                        # Tracciamento ruote per il calcolo delle Ruote Perno e del Calore
                        ruote_rilevate_nel_colpo.extend([ruota1, ruota2])

                        card = {
                            "ruota1": ruota1,
                            "ruota2": ruota2,
                            "num1": pronostico_1,
                            "num2": pronostico_2,
                            "score": score,
                            "dati_r1": " . ".join(map(str, num_r1)),
                            "dati_r2": " . ".join(map(str, num_r2)),
                            "nota_correttiva": nota_correttiva  # Inserita nota nel JSON
                        }
                        card_temporanee.append(card)

        # =======================================================
        # 🛠️ PASSO 1: FILTRAZIONE FINANZIARIA & RUOTA PERNO
        # =======================================================
        # Contiamo le ruote più frequenti per identificare il "Perno" di questo concorso
        conteggio_ruote = Counter(ruote_rilevate_nel_colpo)
        
        # Generiamo la Mappa del Calore (Passo 3) basandoci sul concorso più recente ("nuove")
        if etichetta_colpo == "nuove" and conteggio_ruote:
            max_presenze = max(conteggio_ruote.values()) if conteggio_ruote else 1
            for r in elenco_ruote_valide:
                # Calcolo percentuale di calore da 0 a 100
                presenze = conteggio_ruote.get(r, 0)
                risultati["mappa_calore"][r] = int((presenze / max_presenze) * 100)

        # Determiniamo le 3 ruote perno principali di questa estrazione
        ruote_perno = [coppia[0] for coppia in conteggio_ruote.most_common(3)]

        # Filtriamo le card: diamo priorità assoluta alle card che contengono le Ruote Perno dominanti
        card_filtrate = []
        for card in card_temporanee:
            # Se la card coinvolge almeno una delle ruote perno principali, passa il filtro finanziario
            if card["ruota1"] in ruote_perno or card["ruota2"] in ruote_perno:
                card_filtrate.append(card)

        # Se il filtro è troppo stretto e svuota tutto, teniamo le card originali
        if not card_filtrate:
            card_filtrate = card_temporanee

        # Ordinamento finale per Score decrescente e taglio netto (Massimo 6 card per ripulire lo schermo)
        risultati[etichetta_colpo] = sorted(
            card_filtrate, 
            key=lambda x: x['score'], 
            reverse=True
        )[:6]

    # 3. Scrittura del file risultati aggiornato
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    
    print("Sviluppo LOTTO ELITE PRO V5 completato con successo. Tutti e 3 i passi strategici sono attivi.")

if __name__ == "__main__":
    genera_risultati()
